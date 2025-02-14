from common.models.Campaign import *
from common.dsc import *

from ...local import *

@ACL.include
@arc.slash_command('add-player-to-fabula-campaign', 'dodaje gracza do kampani w systemie fabula')
async def cmd_add_player_to_fabula_campaign(
  ctx: arc.GatewayContext,
  name: arc.Option[str, arc.StrParams('nazwa kampani')],
  user: arc.Option[hikari.User, arc.UserParams('gracz do dodania')],
):
  #
  # security check
  #
  
  campaign : Campaign = FABULA_CAMPAIGN_DB.get_campaign_by_name(name)
  
  if campaign is None:
    await ctx.respond(f"Nie znaleziono kampani w systemie **Fabula Ultima** o nazwie **\"{name}\"**")
  
  if not (str(ctx.author.id) in campaign.gms):
    return await ctx.respond("Nie masz uprawnień aby modyfikować tej kampani palancie")
  
  #
  # security check
  #
  
  if not (str(ctx.author.id) in campaign.gms):
    return await ctx.respond("Nie masz uprawnień aby modyfikować tej kampani palancie")
  
  if not (str(user.id) in campaign.players):
    campaign.players.append(user.id)
    FABULA_CAMPAIGN_DB[name] = campaign
    await ctx.respond(f'dodano gracza {user} do kampani {name}')
  else:
    await ctx.respond(f"gracz {user.global_name} był już w tej kampani")
    
@ACL.include
@arc.slash_command('del-player-from-fabula-campaign', 'usuwa gracza z kampani w systemie Fabula Ultima')
async def cmd_del_player_from_fabula_campaign(  
  ctx: arc.GatewayContext,
  name: arc.Option[str, arc.StrParams('nazwa kampani')],
  user: arc.Option[hikari.User, arc.UserParams('gracz do usunięcia')],
):
  #
  # security check
  #

  campaign : Campaign = FABULA_CAMPAIGN_DB.get_campaign_by_name(name)
  
  if campaign is None:
    await ctx.respond(f"Nie znaleziono kampani w systemie **Fabula Ultima** o nazwie **\"{name}\"**")
  
  if not (str(ctx.author.id) in campaign.gms):
    return await ctx.respond("Nie masz uprawnień aby modyfikować tej kampani palancie")
  
  #
  # security check
  #
  
  userid = str(user.id)
  if str(user.id) in campaign.players:
    off = 0
    for i in range(len(campaign.players)):
      if campaign.players[i - off] == userid:
        campaign.players.pop(i - off)
        off +=1
    FABULA_CAMPAIGN_DB[name] = campaign
    await ctx.respond(f'usunięto gracza {user} z kampani {name}')
  else:
    await ctx.respond(f"gracza {user.global_name} nie było w tej kampani")

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
      await create_campaign_channels_async(ctx.guild_id, name)
        
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
  
  #
  # security check
  #
  
  campaign = FABULA_CAMPAIGN_DB.get_campaign(name)
  if campaign is None:
    return await ctx.respond(f"Nie znaleziono kampani w systemie **Fabula Ultima** o nazwie **\"{name}\"**")
  
  if not (str(ctx.author.id) in campaign.gms):
    return await ctx.respond("Nie masz uprawnień aby modyfikować tej kampani palancie")
  
  #
  # security check
  #
  
  msg = f'poprawinie usunięto kampanie {name}'
  roles = campaign.roles.copy()
  del FABULA_CAMPAIGN_DB[name]
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

  campaign : Campaign = FABULA_CAMPAIGN_DB.get_campaign_by_name(name)
  
  if campaign is None:
    await ctx.respond(f"Nie znaleziono kampani w systemie **Fabula Ultima** o nazwie **\"{name}\"**")

  await ctx.respond(
      tcr.discord.embed(
        tcr.Null,
        f'### Name: {campaign.name} \n system: {campaign.system.value} \n Universe: {campaign.universe} \n GMs: \n{"\n".join(f'- <@{x}>' for x in campaign.gms)}\n\n Players: \n{'\n'.join(f'- <@{x}>' for x in campaign.players)}',
        color=0xF0BFFF,
        footer='uwu',
        author={'name': f'Info - {campaign.name}',"icon": "https://cdn.discordapp.com/attachments/866366097242325016/1209539245673422969/cute-anime-pfp-profile-pictures-girls-29.png?ex=65e74a34&is=65d4d534&hm=b76291968f902ca0ad92962354b9ab748f4d902bbd3ca229ed489dfd0de5bbca&",}
      )
    )