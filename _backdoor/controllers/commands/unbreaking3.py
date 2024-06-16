from _backdoor.local.consts import SERWER_ANTKA

from common.dsc import *
from common.models.Command import Command

@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_unbreaking3(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return

    try:
        command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)
        
        if command.prefix() == "!rpg" and command.command() == 'bring-back-fun':
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
