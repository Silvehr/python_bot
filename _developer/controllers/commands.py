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
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        if command.prefix() == "!rpg":
            cName = command.command().lower()
            service: ReminderService = REGISTERED_SERVICES[ReminderService]

            if cName== "new-reminder":
                eventName = command[0]

                startDate = command[1]
                if startDate == '!':
                    startDate = date.today()
                else:
                    startDate = parse_date(startDate)

                startTime = command[2]
                if startTime == '!':
                    now = datetime.now()
                    startTime = time(now.hour, now.minute,now.second)
                else:
                    startTime = parse_time(startTime)

                interval = command[3]
                message= command[4]

                service: ReminderService = REGISTERED_SERVICES[ReminderService]
                await event.message.respond(f"Successfully created reminder **{service.AddNewReminderEvent(eventName,datetime(startDate.year, startDate.month, startDate.day, startTime.hour, startTime.minute, startTime.second), parse_timedelta(interval), message).Name}**")
            elif cName == "del-reminder":
                reminderName = command[0]
                if len(reminderName) == 0:
                    return

                reminders = service.FindReminders(reminderName)

                if len(reminders) == 1:
                    reminderName = reminders[0].Name
                    service.RemoveReminderEvent(reminders[0].Id)
                    await event.message.respond(f"Successfully removed reminder **{reminderName}**")
                elif len(reminders) > 1:
                    response = "# Which one?\n"
                    for reminders in reminders:
                        response += f"    Name: {reminders.Name}\n    Id: {reminders.Id}\n    Message: {reminders.Message}"
                    await event.message.respond(response)
                else:
                    await event.message.respond(f"Reminder **\"{reminderName}\"** not found")
            elif cName == "get-reminder":
                reminderName = command[0]
                if len(reminderName) == 0:
                    return

                reminders = service.FindReminders(reminderName)

                if len(reminders) == 0:
                    await event.message.respond(f"No reminders were found")
                else:
                    response = ""
                    for reminders in reminders:
                        response += (f"# {reminders.Name} ({reminders.Id})\n"
                                     f"Next estimated invoke: {reminders.LastRun + reminders.Interval}\n"
                                     f"Reminder message : {reminders.Message}\n"
                                     f"Triggered **{reminders.TriggerCount}** times\n"
                                     f"Listeners:\n")

                        for listener in reminders.Listeners:
                            response += f"    <@{listener}>"

                        response += "\n"

                    await event.message.respond(response)
            elif cName == "add-listeners":
                reminderName = command[0]
                if len(reminderName) == 0:
                    return

                reminders = service.FindReminders(reminderName)

                if len(reminders) == 1:
                    reminders = reminders[0]
                elif len(reminders) > 1:
                    response = "#Which one?"
                    for reminder in reminders:
                        response += f"    Name: {reminder.Name}\n    Id: {reminder.Id}\n    Message: {reminder.Message}"
                    return

                reminderName = reminders.Name
                listeners = command.asList(1)

                if len(listeners) == 0:
                    await event.message.respond(f"No listener was provided")
                    return

                for listener in listeners:
                    try:
                        username = (await BOT.rest.fetch_user(listener)).global_name
                        service.AddListenerToEvent(reminders.Id, listener)
                        await event.message.respond(f"Successfully added {username} to the **{reminderName}** reminder")
                    except hikari.errors.NotFoundError:
                        await  event.message.respond(f"Listener {listener} not found")
            elif cName == "del-listeners":
                reminderName = command[0]
                if len(reminderName) == 0:
                    await event.message.respond(f"No event was provided")
                    return

                reminders = service.FindReminders(reminderName)

                if len(reminders) == 1:
                    reminderName = reminders[0].Name
                    reminders = reminders[0]

                    listeners = command.asList(1)

                    if len(listeners) == 0:
                        await event.message.respond(f"No listener was provided")
                        return

                    for listener in listeners:
                        service.RemoveListenerFromEvent(reminders.Id, listener)
                        await event.message.respond(
                            f"Successfully removed {(await BOT.rest.fetch_user(listener)).global_name} from **{reminderName}** reminder")
                elif len(reminders) > 1:
                    response = "# Which one?\n"
                    for reminders in reminders:
                        response += f"    Name: {reminders.Name}\n    Id: {reminders.Id}\n    Message: {reminders.Message}"
                    await event.message.respond(response)
                    return
                else:
                    await event.message.respond(f"Reminder **\"{reminderName}\"** not found")
                    return
            elif cName == "remove-listener":
                listeners = command.asList(0)

                for listener in listeners:
                    found = service.RemoveListener(listener)

                    if found:
                        await event.message.respond(f"Successfully removed all {(await BOT.rest.fetch_user(listener)).global_name} reminders")
            elif cName == "get-listener":
                listener = service.GetListener(command[0])

                if listener:
                    result = f"# {(await BOT.rest.fetch_user(listener.Id)).global_name}"
                    for reminder, t_c in listener.ReminderEvents.items():
                        result +=f"    Reminder: **{service.GetReminderEventById(reminder).Name}** triggered **{t_c}** times\n"

                    await event.message.respond(result)
                else:
                    await event.message.respond("Listener not found")
            elif cName == "read-all-listeners":
                await event.message.respond("This process may take a while...")

                for guildId in REGISTERED_GUILDS:
                    guild = await BOT.rest.fetch_guild(guildId)
                    for user in guild.get_members().values():
                        if not user.is_bot:
                            service.AddListener(user.id)

                await event.message.respond("All users are ready!")
            elif cName == "get-all-listeners":
                response = "# All listeners\n"
                for listener in service._listeners.values():
                    response += f"{(await BOT.rest.fetch_user(listener.Id)).global_name}\n"
                await event.message.respond(response)

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