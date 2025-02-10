from ...local import *

from common.dsc.gateways import *
from common.models.Command import Command
from common.env.consts import *

import datetime

@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_send_to_a_break(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        
        if command.prefix() == "!rpg" and command.command() == 'send-to-a-break':
            user : str = command.get_argument(0)
            guild : str = command.get_argument(1)
            time : str = command.get_argument(2) #yyyy:mm:dd:hh:mm:ss
            member : hikari.Member

            if len(guild) == 0:
                time = guild
                guild = SERWER_ANTKA #serwer Antka

            if len(user) == 0 or user.lower() == 'antek':
                user = ANTEK #Antek

            if len(time) == 0 or time == "!":
                time = datetime(datetime.now().year,datetime.now().month,datetime.now().day + 1,datetime.now().hour,datetime.now().minute,datetime.now().second,0)
            else:
                time_syntax_tree = time.replace(" ","").split(":")
                for i in range(len(time_syntax_tree)):
                    time_syntax_tree[i] = int(time_syntax_tree[i])
                
                time = datetime(datetime.now().year + time_syntax_tree[0], datetime.now().month + time_syntax_tree[1], datetime.now().day + time_syntax_tree[2], time_syntax_tree[1], datetime.now().hour + time_syntax_tree[3], time_syntax_tree[1], datetime.now().minute + time_syntax_tree[4], time_syntax_tree[1], datetime.now().second + time_syntax_tree[5])
            member = await BOT.rest.fetch_member(guild=guild, user=user)  
            await member.edit(communication_disabled_until=time)
            await event.message.respond(f"fun breaker ({member.global_name}) breaked")
            
    except Exception as e:
        channel = await BOT.rest.create_dm_channel(MEINID)
        await channel.send(str(e))
        raise

@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_unbreaking3(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return

    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        
        if command.prefix() == "!rpg" and command.command() == 'take-back-from-break':
            user = command.get_argument(0)
            guild = command.get_argument(1)

            if len(guild) == 0:
                guild = SERWER_ANTKA

            member : hikari.Member
            if(user):
                member = await BOT.rest.fetch_member(guild=guild, user=user)
            else: 
                member = await BOT.rest.fetch_member(guild=guild, user=event.author_id)

            await member.edit(communication_disabled_until=None)
            await event.message.respond(f"unbreaked {member.global_name}", flags=hikari.MessageFlag.EPHEMERAL)

    except Exception as e:
        channel = await BOT.rest.create_dm_channel(569608391840759837)
        await channel.send(str(e))
        raise
