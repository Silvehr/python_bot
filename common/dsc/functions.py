from hikari import *
from .gateways import *

async def create_campaign_channels_async(guild_id: Snowflake, name: str):
    category = await BOT.rest.create_guild_category(guild_id, name)
    await BOT.rest.create_guild_text_channel(guild_id, 'ogólne', category=category)
    await BOT.rest.create_guild_text_channel(guild_id, 'rzeczy-kampaniowe', category=category)
    await BOT.rest.create_guild_text_channel(guild_id, 'funny', category=category)
    await BOT.rest.create_guild_text_channel(guild_id, 'kpeki', category=category)
    await BOT.rest.create_guild_text_channel(guild_id, 'komendy-i-pierwiastki', category=category)
    await BOT.rest.create_guild_voice_channel(guild_id, 'sesja', category=category)
    await BOT.rest.create_guild_voice_channel(guild_id, 'spiskowo', category=category)
    
def get_id_from_ping(discord_ping_content : str):
    return discord_ping_content[2:len(discord_ping_content) - 1]
    