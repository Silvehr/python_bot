from _backdoor.local.consts import *
from ...models.EA_Client import EA_Client

from common.dsc import *
from common.models.Command import Command

import tcrutils as tcr


@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_ea_mode(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        
        if command.prefix() == "!rpg" and command.command() == 'ea-mode':
            action = command.get_argument(0)
            user = command.get_argument(1)
            guild = command.get_argument(2)
            
            if(len(user) == 0):
                user = ANTEK
            
            if(len(guild) == 0):
                user = ANTEK
                guild = SERWER_ANTKA
                
            if not (user in EA_MODE_CLIENTS):
                EA_MODE_CLIENTS[user] = EA_Client(user)
                
                
            if action.lower() == "enable":
                client = EA_MODE_CLIENTS[user]
                client.enable()
                EA_MODE_CLIENTS[user] = client
                await event.message.respond(f"User **{(await BOT.rest.fetch_member(guild=guild, user=user)).global_name}** is an EA Client now on server **{(await BOT.rest.fetch_guild(guild)).name}**")
            elif action.lower() == "disable":
                client = EA_MODE_CLIENTS[user]
                client.disable()
                EA_MODE_CLIENTS[user] = client
                await event.message.respond(f"User **{(await BOT.rest.fetch_member(guild=guild, user=user)).global_name}** is **not** an EA Client now on server **{(await BOT.rest.fetch_guild(guild)).name}**")
            else:
                await event.message.respond(f"Ambigous option \"{action}\"")
        
    except Exception as e:
        channel = await BOT.rest.create_dm_channel(569608391840759837)
        print(str(e))
        await channel.send(str(e))
        raise