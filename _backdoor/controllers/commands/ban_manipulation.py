from common.dsc.gateways import *
from common.models.Command import *

@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_unban(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        
        if command.prefix() == "!rpg" and command.command() == 'unban':
            user : str = command.get_argument(0)
            guild = command.get_argument(1)
            
            guild = await BOT.rest.fetch_guild(guild=guild)
            user = await BOT.rest.fetch_user(user)
            await guild.unban(user=user)
            
            await event.message.respond(f"przywrócono użytkownika {user.global_name} do serwera {guild.name}")
        
    except hikari.NotFoundError:
        await event.message.respond("Nie znaleziono kampani lub użytkownika")
    
    except hikari.UnauthorizedError:
        await event.message.respond("Bot nie ma uprawnień aby to zrobić")
    except Exception:
        await event.message.respond("Nie oczekiwany błąd")
        
@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_ban(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        
        if command.prefix() == "!rpg" and command.command() == 'ban':
            user = command.get_argument(0)
            guild = command.get_argument(1)
            
            guild = await BOT.rest.fetch_guild(guild=guild)
            user = await BOT.rest.fetch_user(user)
            await guild.ban(user=user)
            
            await event.message.respond(f"zbanowano użytkownika {user.global_name} z serwera {guild.name}")
        
    except hikari.NotFoundError:
        await event.message.respond("Nie znaleziono kampani lub użytkownika")
        
    except hikari.UnauthorizedError:
        await event.message.respond("Bot nie ma uprawnień aby to zrobić")
        
    except Exception:
        await event.message.respond("Nie oczekiwany błąd")