from common.models.Campaign import *
from common.dsc import *

from _fate.local.consts import *

import tcrutils as tcr

@ACL.include
@arc.slash_command('create-fate-campaign', 'tworzy kampanię w systemie fate')
async def cmd_add_campaign_fate(  
    ctx: arc.GatewayContext,
    channels: arc.Option[bool, arc.BoolParams('czy tworzyć kanały?')],
    name: arc.Option[str, arc.StrParams('Nazwa kampani')],
    universe: arc.Option[str, arc.StrParams('uniwersum')],
    gms: arc.Option[str, arc.StrParams('Id mistrzów gry rozdzielane ,')],
    players: arc.Option[str, arc.StrParams('Id graczy rozdzielane ,')],
):
    gms = gms.strip().split(',')
    players = players.strip().split(', ')
    try:
        system = CampaignSystem(system.lower())
    except ValueError:
        return await ctx.respond(f'Nie ma takiego systemu debilu')
    if not all(tcr.discord.is_snowflake(x, allow_string=True) for x in players):
        return await ctx.respond('id players to nie sa prawidlowe id discordowe debilu (to nie prawidłowy snowflake)')
    if not all(tcr.discord.is_snowflake(x, allow_string=True) for x in gms):
        return await ctx.respond('id gms to nie sa prawidlowe id discordowe debilu (to nie prawidłowy snowflake)')
    gm_role = await BOT.rest.create_role(ctx.guild_id, name=f'GM - {name}', color='#fd04f8')
    player_role = await BOT.rest.create_role(ctx.guild_id, name=f'Gracz - {name}', color='#6AFD04')
    if channels:
        category = await BOT.rest.create_guild_category(ctx.guild_id, name)
        await BOT.rest.create_guild_text_channel(ctx.guild_id, 'ogólne', category=category)
        await BOT.rest.create_guild_text_channel(ctx.guild_id, 'rzeczy-kampaniowe', category=category)
        await BOT.rest.create_guild_text_channel(ctx.guild_id, 'funny', category=category)
        await BOT.rest.create_guild_text_channel(ctx.guild_id, 'kpeki', category=category)
        await BOT.rest.create_guild_text_channel(ctx.guild_id, 'komendy-i-pierwiastki', category=category)
        await BOT.rest.create_guild_voice_channel(ctx.guild_id, 'sesja', category=category)
        await BOT.rest.create_guild_voice_channel(ctx.guild_id, 'spiskowo', category=category)
    campaign = Campaign(name, system, universe, gms, players, roles=[gm_role.id, player_role.id])
    FATE_CAMPAIGN_DB[name] = campaign
    gm_errors = []
    for id in gms:
        try:
            member = await BOT.rest.fetch_member(ctx.guild_id, int(id))
            await member.add_role(gm_role)
        except hikari.NotFoundError:
            gm_errors.append(id)
    player_errors = []
    for id in players:
        try:
            member = await BOT.rest.fetch_member(ctx.guild_id, int(id))
            await member.add_role(player_role)
        except hikari.NotFoundError:
            player_errors.append(id)
    msg = f'Pomyślnie stworzono kampanie {name}'
    if gm_errors:
        msg += '\n:x: Wystapil blad podczas dodawania roli GM dla tych uzytkownikow: ' + ', '.join(f'<@{x}>' for x in gm_errors)
    if player_errors:
        msg += '\n:x: Wystapil blad podczas dodawania roli graczy dla tych uzytkownikow: ' + ', '.join(f'<@{x}>' for x in player_errors)
    await ctx.respond(msg)