from common.models.Command import Command
from common.dsc import *

from _resources.local.consts import *

@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_resource(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        if(command.prefix() == "!rpg"):
            
            if command.command() == "get":
                try:
                    resource = RESOURCES[command.get_argument(0)]
                    if(resource.is_file):
                        await event.message.respond(resource.full_name, attachment=hikari.File(resource.url))
                    else:
                        await event.message.respond(resource.full_name, attachment=hikari.URL(resource.url))
                except KeyError:
                    await event.message.respond(f"Nie posiadam zasobu o nazwie \"{command.get_argument(0)}\"")
            elif command.command() == "list-resources":
                await event.message.respond('**!RPG komendy** \n "fabula-podr" - podręcznik do Fabula Ultima \n "fate-podr" - podręcznik do Fate Core \n "cyberpunk-podr" - podręcznik do Cyberpunk Red \n "fabula-kp" - Karta postaci do Fabula Ultima \n "fate-kp" - Karta postaci do Fate core \n "cyberpunk-kp" - Karta postaci do Cyberpunk Red \n "fate-skills" - umiejki fate \n "fate-stunts" - strona do sztuczek Fate Core')
            
            
    except Exception as e:
        channel = await BOT.rest.create_dm_channel(569608391840759837)
        await channel.send(str(e)) 
        raise