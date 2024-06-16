from common.dsc import *
from common.models.Command import Command

@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_ping(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        
        if command.prefix() == "!rpg" and command.command() == 'ping':
            await event.message.respond("active")
            
    except Exception as e:
        channel = await BOT.rest.create_dm_channel(569608391840759837)
        await channel.send(str(e))
        raise