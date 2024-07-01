from ...._backdoor.local import *
from ...._backdoor.models import *

from common.dsc.gateways import *
from common.models.Command import Command
from common.dsc.functions import *

@BOT.listen(hikari.GuildMessageCreateEvent)
async def analysis_of_user_as_text(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        
        if command.prefix() == "!rpg" and command.command() == 'analize-ping':
            await event.message.respond(get_id_from_ping(command.get_argument(0)))
            
        
    except Exception as e:
        await LOGGER.log_error(e)
        raise
    
@BOT.listen(hikari.GuildMessageCreateEvent)
async def raise_exception(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        
        if command.prefix() == "!rpg" and command.command() == 'raise-exception':
            raise ForcedException("ForcedException raised")
            
    except Exception as e:
        await LOGGER.log_error(e)
        
@ACL.include
@arc.slash_command("ping", "Komenda do weryfikacji aktywności bota")
async def cmd_ping(ctx: arc.GatewayContext):
  return await ctx.respond("pong!")
    