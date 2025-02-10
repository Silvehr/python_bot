from common.dsc.gateways import *
from common.dsc.consts import *
from common.models.Command import *
from common.env.consts import *
from _developer.local.db import *
from _developer.models.reminder_service import *
from common.models.date_parse import  *
from common.services import REGISTERED_SERVICES

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
async def set_reminder(event: hikari.DMMessageCreateEvent):
    if event.is_bot or not event.content:
        return

    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)

        if command.prefix() == "!rpg":
            if command.command() == "set-reminder":
                user_id = command.get_argument(0)
                start_d = command.get_argument(1)
                if start_d == '!':
                    start_d = date.today()
                else:
                    start_d = parse_date(start_d)

                start_t = command.get_argument(2)

                if start_t == '!':
                    now = datetime.now()
                    start_t = time(now.hour, now.minute,now.second)
                else:
                    start_t = parse_time(start_t)
                interval = command.get_argument(3)
                message= command.get_argument(4)

                service_user = ReminderClient(user_id, datetime(start_d.year,start_d.month,start_d.day,start_t.hour,start_t.minute,start_t.second), parse_timedelta(interval),message)
                service: ReminderService = REGISTERED_SERVICES["ReminderService"]
                await service.add_client(service_user)
            elif command.command() == "rm-reminder":
                user_id = command.get_argument(0)
                service: ReminderService = REGISTERED_SERVICES["ReminderService"]
                service.remove_client(user_id)

    except:
        channel = await BOT.rest.create_dm_channel(MEINID)



loop_protection = True

@BOT.listen()
async def loop_protection_down(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
    if command.prefix() == "!rpg" and command.command() == "loop-protection-down":
        loop_protection = False

@BOT.listen()
async def loop_protection_up(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
    if command.prefix() == "!rpg" and command.command() == "loop-protection-up":
        loop_protection = True
    

@BOT.listen()
async def loop(event: hikari.GuildMessageCreateEvent):
    if (event.is_bot or not event.content) and loop_protection:
        return
    
    command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
    if command.prefix() == "loop":
        event.message.respond("loop")