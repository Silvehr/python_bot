from hikari import *
from .gateways import *
from typing import Callable, Iterable, Literal
import re as regex

async def create_campaign_channels_async(guild_id: Snowflake, name: str):
    category = await BOT.rest.create_guild_category(guild_id, name)
    await BOT.rest.create_guild_text_channel(guild_id, 'ogólne', category=category)
    await BOT.rest.create_guild_text_channel(guild_id, 'rzeczy-kampaniowe', category=category)
    await BOT.rest.create_guild_text_channel(guild_id, 'funny', category=category)
    await BOT.rest.create_guild_text_channel(guild_id, 'kpeki', category=category)
    await BOT.rest.create_guild_text_channel(guild_id, 'komendy-i-pierwiastki', category=category)
    await BOT.rest.create_guild_voice_channel(guild_id, 'sesja', category=category)
    await BOT.rest.create_guild_voice_channel(guild_id, 'spiskowo', category=category)

async def get_discord_user(identifier: str, invoker: hikari.users.User) -> hikari.users.User | None:
    if identifier[0] == "<" and identifier[-1] == ">" and identifier[1] == "@":
        identifier = identifier[2:-1]

    elif identifier.lower() == "me":
        identifier = str(invoker.id)

    try:
        return await BOT.rest.fetch_user(identifier)
    except hikari.errors.NotFoundError:
        return None

async def try_response(message: hikari.messages.Message, defaultAnswer: str, backupAnswer: str) -> bool:
    try:
        await message.respond(defaultAnswer)
    except hikari.errors.BadRequestError:
        try:
            await message.respond(backupAnswer)
        except:
            return False
    except:
        return False

    return True

    