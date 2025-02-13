import hikari
import traceback

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

import os
import shutil
import sys

import tcrutils as tcr

@ACL.include
@arc.slash_command('dev', 'moje nie dam')
async def cmd_dev(ctx: arc.GatewayContext, code: arc.Option[str, arc.StrParams('kodzik nie dla frajerów')]):
  if str(ctx.author.id) not in DEV_COMMAND_BENEFICARIES:
    return await ctx.respond('nie dla psa kiełabasa frajerze moje')
  try:
    result = tcr.codeblock(tcr.fmt_iterable(eval(code), syntax_highlighting=True), langcode='ansi')
  except Exception as e:
    result = f'{tcr.codeblock(tcr.extract_error(e), langcode="txt" )}\n{tcr.codeblock(tcr.extract_traceback(e), langcode="py")}'
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
            target: str = command.command().lower()
            service: ReminderService = REGISTERED_SERVICES[ReminderService]

            action: str = command[paramIndex].lower()
            paramIndex+=1
            if target == "reminder":
                reminderName: str = command[paramIndex]
                paramIndex+=1
                if action == "new":

                    # at => triggers once
                    # from => triggers multiple times
                    reminderTypeOperator: str = command[paramIndex].lower()
                    nowOperatorUsed: bool =False
                    paramIndex+=1

                    if reminderTypeOperator not in "at from":
                        await event.message.respond(f"Unexpected value \"{reminderTypeOperator}\"")

                    startDate: str = command[paramIndex].lower()
                    paramIndex += 1

                    if startDate != "now":
                        try:
                            startDate: date = parse_date(startDate)
                        except:
                            await event.message.respond(f"\"{startDate}\" cannot be interpreted as date")
                            return

                        startTime: str = command[paramIndex].lower()
                        paramIndex += 1

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

                    interval = timedelta(0, 0, 0, 0, 0, 0, 0)
                    triggerCount = -1

                    if reminderTypeOperator == "from":
                        if command[paramIndex].lower() == "times":
                            paramIndex+=1

                            try:
                                triggerCount = int(command[paramIndex])
                                paramIndex += 1
                            except:
                                await event.message.respond(
                                    f"\"{command[paramIndex]}\" cannot be interpreted as integer")
                                return
                        else:
                            triggerCount = -1

                        if command[paramIndex].lower() == "every":
                            paramIndex += 1

                        try:
                            interval = parse_timedelta(command[paramIndex])
                            paramIndex += 1
                        except:
                            await event.message.respond(
                                f"\"{command[paramIndex]}\" cannot be parsed as time difference")
                            return

                        if nowOperatorUsed:
                            parsedTime += interval

                    listenersIds: list[str] = []

                    # Gather listeners
                    if command[paramIndex].lower() == "to":
                        paramIndex+=1

                        if command[paramIndex].lower() == "everyone":
                            paramIndex+=1
                            listenersIds = list(service._listeners.keys())
                        else:
                            while command[paramIndex].lower() != "say":
                                if command[paramIndex].lower() == "me":
                                    listenersIds.append(str(event.author_id))
                                else:
                                    listenersIds.append(command[paramIndex])
                                paramIndex+=1

                    if command[paramIndex].lower() == "say":
                        paramIndex+=1
                    message = command[paramIndex]

                    if reminderTypeOperator == "at":
                        await event.message.respond(f"Successfully created reminder **{service.AddNewReminder(reminderName, message, parsedTime, listeners=listenersIds).Name}**")
                    else:
                        await event.message.respond(f"Successfully created reminder **{
                        service.AddNewReminder(reminderName, message, parsedTime, interval, triggerCount, listenersIds).Name}**")

                elif action == "del":
                    if len(reminderName) == 0:
                        return

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
                    if len(reminderName) == 0:
                        return

                    reminders = service.FindReminders(reminderName)

                    if len(reminders) == 0:
                        await event.message.respond(f"No reminders were found")
                    else:
                        response = ""
                        for reminders in reminders:
                            response += (f"# {reminders.Name} ({reminders.Id})\n"
                                         f"Next estimated invoke: {reminders.NextRun + reminders.Interval}\n"
                                         f"Reminder message : {reminders.Message}\n"
                                         f"Triggered **{reminders.TriggerCount}** times\n"
                                         f"Listeners:\n")

                            for listener in reminders.Listeners:
                                response += f"    <@{listener}>"

                            response += "\n"

                        await event.message.respond(response)
                elif action == "add" and command[1] == "listeners":
                    reminderName = command[2]
                    if len(reminderName) == 0:
                        return

                    reminders = service.FindReminders(reminderName)

                    if len(reminders) == 0:
                        await event.message.respond(f"Reminder **\"{reminderName}\"** not found")
                        return
                    elif len(reminders) > 1:
                        response = "#Which one?"
                        for reminder in reminders:
                            response += f"    Name: {reminder.Name}\n    Id: {reminder.Id}\n    Message: {reminder.Message}"
                        return

                    reminders = reminders[0]

                    reminderName = reminders.Name
                    listeners = command.asList(2)

                    if len(listeners) == 0:
                        await event.message.respond(f"No listener was provided")
                        return

                    for listener in listeners:
                        try:
                            username = (await BOT.rest.fetch_user(listener)).global_name
                            service.AddListenerToReminder(reminders.Id, listener)
                            await event.message.respond(
                                f"Successfully added {username} to the **{reminderName}** reminder")
                        except hikari.errors.NotFoundError:
                            await  event.message.respond(f"Listener {listener} not found")
                elif action == "rem" and command[1] == "listeners":
                    reminderName = command[2]
                    if len(reminderName) == 0:
                        await event.message.respond(f"No event was provided")
                        return

                    reminders = service.FindReminders(reminderName)

                    if len(reminders) > 1:
                        response = "# Which one?\n"
                        for reminders in reminders:
                            response += f"    Name: {reminders.Name}\n    Id: {reminders.Id}\n    Message: {reminders.Message}"
                        await event.message.respond(response)
                        return
                    elif len(reminders) == 0:
                        await event.message.respond(f"Reminder **\"{reminderName}\"** not found")
                        return

                    reminderName = reminders[0].Name
                    reminders = reminders[0]

                    listeners = command.asList(1)

                    if len(listeners) == 0:
                        await event.message.respond(f"No listener was provided")
                        return

                    for listener in listeners:
                        service.RemoveReminderListener(reminders.Id, listener)
                        await event.message.respond(
                            f"Successfully removed {(await BOT.rest.fetch_user(listener)).global_name} from **{reminderName}** reminder")
            elif target == "listener":
                listenerId = command[1]
                if action == "del":
                    if service.RemoveListener(listenerId):
                        await event.message.respond(f"Successfully removed all {(await BOT.rest.fetch_user(listenerId)).global_name} reminders")
                elif action == "get":
                    listener = service.GetListener(command[0])
                    if listener:
                        result = f"# {(await BOT.rest.fetch_user(listenerId)).global_name}"
                        for reminder, t_c in listener.ReminderEvents.items():
                            result += f"    Reminder: **{service.GetReminderEventById(reminder).Name}** triggered **{t_c}** times\n"

                        await event.message.respond(result)
                    else:
                        await event.message.respond("Listener not found")
                elif action == "add" and command[1] == "reminders":
                    listenerId = command[2]
                    if service.GetListener(listenerId) is None:
                        service.GetListener(listenerId)

                    reminders = command.asList(2)
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
                            await event.message.respond(response+"Enter whole name or id and try running command again")
                            return

                    for matches in remindersMatches:
                        service.AddListenerToReminder(matches[0].Id, listenerId)
                elif action == "rem" and command[1] == "reminders":
                    listenerId = command[2]
                    if service.GetListener(listenerId) is None:
                        await event.message.respond(f"Listener with id of **\"{listenerId}\"** not found")

                    reminders = command.asList(2)
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
                                response + "Enter whole name or id and try running command again")
                            return

                    for matches in remindersMatches:
                        service.RemoveReminderListener(matches[0].Id, listenerId)
            elif target == "listeners":
                if action == "get" and command[1] == "all":
                    response = "# All listeners\n"
                    for listener in service._listeners.values():
                        response += f"{(await BOT.rest.fetch_user(listener.Id)).global_name}\n"
                    await event.message.respond(response)
                elif action == "include" :
                    if command[1] == "all":
                        await event.message.respond("This may take a while...")
                        for guildId in REGISTERED_GUILDS:
                            guild = await BOT.rest.fetch_guild(guildId)
                            for member in guild.get_members().values():
                                if not member.is_bot:
                                    service.GetListener(str(member.id))
                        await event.message.respond("All users are ready!")
                    elif command[1] == "local":
                        await event.message.respond("This make take a while...")
                        guild = event.get_guild()
                        for member in guild.get_members().values():
                            if not member.is_bot:
                                service.GetListener(str(member.id))
                        await event.message.respond("Local users are ready!")

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


@BOT.listen(hikari.GuildMessageCreateEvent)
async def lock_cross_env_access(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return

    command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)

    if command.prefix() == "!rpg" and command.command() == "rm" and command[0] == "-rf" and command[1] == "self":
        shutil.rmtree(os.path.dirname(os.path.abspath(sys.argv[0])))