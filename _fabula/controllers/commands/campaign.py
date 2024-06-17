from common.models.Campaign import *
from common.dsc import *

from ...local import *

import tcrutils as tcr

@ACL.include
@arc.slash_command('add-player-to-fabula-campaign', 'dodaje gracza do kampani w systemie fabula')
async def cmd_add_player_to_fabula_campaign(
  ctx: arc.GatewayContext,
  name: arc.Option[str, arc.StrParams('nazwa kampani')],
  user: arc.Option[hikari.User, arc.UserParams('gracz do dodania')],
):
  campaign = FABULA_CAMPAIGN_DB[name]
  if not (str(user.id) in campaign.players):
    campaign.players.append(user.id)
  FABULA_CAMPAIGN_DB[name] = campaign
  await ctx.respond(f'dodano gracza {user} do kampani {name}')

@ACL.include
@arc.slash_command('create-fabula-campaign', 'tworzy kampanię w systemie fabula')
async def cmd_create_fabula_campaign(  
    ctx: arc.GatewayContext,
    channels: arc.Option[bool, arc.BoolParams('czy tworzyć kanały?')],
    name: arc.Option[str, arc.StrParams('Nazwa kampani')],
    universe: arc.Option[str, arc.StrParams('uniwersum')],
    gms: arc.Option[str, arc.StrParams('Id mistrzów gry rozdzielane ,')],
    players: arc.Option[str, arc.StrParams('Id graczy rozdzielane ,')],
):
    gms = gms.strip().split(',')
    players = players.strip().split(', ')
    
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
        
    FABULA_CAMPAIGN_DB[name] = Campaign(name, CampaignSystem.FATE, universe, gms, players, roles=[gm_role.id, player_role.id])
    
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
    
@ACL.include
@arc.slash_command('del-fabula-campaign', 'usuwa kampanie w systemie fabula')
async def cmd_del_fabula_campaign(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('nazwa kampani')]):
  msg = f'poprawinie usunięto kampanie {name}'
  if name in FABULA_CAMPAIGN_DB:
    roles = FABULA_CAMPAIGN_DB[name].roles.copy()
    del FABULA_CAMPAIGN_DB[name]
  else:
    return await ctx.respond('nie ma takiej kampani')
  guild = ctx.get_guild()
  channels = guild.get_channels()
  categories = {cid: ch for cid, ch in channels.items() if ch.type == hikari.ChannelType.GUILD_CATEGORY}
  try:
    category_to_delete = [x for x in categories.values() if x.name == name][0]
  except IndexError:
    msg += '\n :x: nie ma kategori do usunięcia'
  else:
    channels_to_delete = [ch for ch in channels.values() if ch.parent_id == category_to_delete.id]
    await category_to_delete.delete()
    for channel in channels_to_delete:
      await channel.delete()
    guildroles = await BOT.rest.fetch_roles(guild=guild)
    roles_to_delete = [x for x in guildroles if x.id in roles]
    for role in roles_to_delete:
      await BOT.rest.delete_role(guild=guild,role=role)
  await ctx.respond(msg)

@ACL.include
@arc.slash_command('show-fabula-campaign', 'pokazuje info o kampani')
async def cmd_show_fabula_campaign(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('nazwa kampani')]):
  try:
    campaign = FABULA_CAMPAIGN_DB[name]
  except KeyError:
    return await ctx.respond('keep yourself safe nie ma takiej kampani')
  await ctx.respond(
    tcr.discord.embed(
      tcr.Null,
      f'### Name: {campaign.name} \n system: {campaign.system.value} \n Universe: {campaign.universe} \n GMs: \n{'\n'.join(f'- <@{x}>' for x in campaign.gms)}\n\n Players: \n{'\n'.join(f'- <@{x}>' for x in campaign.players)}',
      color=0xF0BFFF,
      footer='uwu',
      author={
        'name': f'Info - {campaign.name}',
        'icon': 'https://cdn.discordapp.com/attachments/866366097242325016/1209539245673422969/cute-anime-pfp-profile-pictures-girls-29.png?ex=65e74a34&is=65d4d534&hm=b76291968f902ca0ad92962354b9ab748f4d902bbd3ca229ed489dfd0de5bbca&',
      },
    )
  )