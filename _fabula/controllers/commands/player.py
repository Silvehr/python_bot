from common.dsc.gateways import *
from _fabula.models import *
from _fabula.local import *

from common.functions import *

import tcrutils as tcr

@ACL.include
@arc.slash_command('create-fabula-player', 'tworzy gracza fabula')
async def cmd_create_fabula_player(
  ctx: arc.GatewayContext,
  name: arc.Option[str, arc.StrParams('imie postaci')],
  attributes: arc.Option[str, arc.StrParams('atrybuty twojej postaci (DEX, INS, MIG, WLP)')],
  identity: arc.Option[str, arc.StrParams('Identity postaci')],
  origin: arc.Option[str, arc.StrParams('origin postaci')],
  theme: arc.Option[str, arc.StrParams('theme twojej postaci')],
  clevel: arc.Option[int, arc.IntParams('poziom postaci')],
  stats: arc.Option[str, arc.StrParams('statystyki HP MP IP DEF MDEF')],
  character_class: arc.Option[str, arc.StrParams('klasy postaci')],
  user: arc.Option[hikari.User, arc.UserParams('gracz do postaci')] = None,
):
  if user is None:
    user = ctx.user
  
  attributes = attributes.split(',')
  dict_attributes = {}
  
  for x in attributes:
    x = x.strip().split(" ")
    dict_attributes[x[0].upper()] = int(x[1])
  
  stats = stats.split(',')
  dict_stats = {}
  
  for x in stats:
    x = x.strip().split(" ")
    dict_stats[x[0].upper()] = int(x[1])
  
  character_class = character_class.split(',')
  fabula_player = FabulaPlayer(name, identity, origin, theme, dict_attributes, clevel, dict_stats, character_class, 0)
  FABULA_PLAYER_DB[str(user.id)] = fabula_player
  
  await ctx.respond(f'Pomyślnie stworzono postać {name} w systemie **Fabula Ultima**')
  
@ACL.include
@arc.slash_command('del-fabula-player', 'usuwa gracza fabula')
async def cmd_del_fabula_player(ctx: arc.GatewayContext):

  player = FABULA_PLAYER_DB.get_player(ctx.user.id)

  if player is None:
    return await ctx.respond("Nie posiadasz postaci w bazie postaci **Fabula Ultima**")
  
  del FABULA_PLAYER_DB[ctx.user.id]

  return await ctx.respond(f"Pomyślnie usunięto {player.name} z bazy postaci **Fabula Ultima**")

@ACL.include
@arc.slash_command('edit-fabula-character', 'edytuje konkretny element postaci w systemie fabula')
async def cmd_edit_fabula_character(ctx: arc.GatewayContext,element: arc.Option[str, arc.StrParams('element do edycji', choices=list(FabulaPlayer.__annotations__))], value: arc.Option[str, arc.StrParams('nowa zawartosc')], name: arc.Option[str, arc.StrParams('Imie postaci')] = None):
  owner : str
  player : FabulaPlayer
  
  if name:
    pair = FABULA_PLAYER_DB.get_pair_by_value_attrs({"name" : name})

    if pair is None:
      return await ctx.respond(f"Nie ma graczy o imieniu {name} w bazie graczy **Fabula Ultima**")
    else:
      owner = pair[0]
      player = pair[1]
  else:
    owner = ctx.user.id
    player = FABULA_PLAYER_DB.get_player(owner)
    
    if player is None:
      return await ctx.respond("Nie jesteś zarejestrowany/zarejestrowana w bazie graczy systemu **Fabula Ultima**")
  
  player.__setattr__(element, value)
  FABULA_PLAYER_DB[owner] = player
  await ctx.respond(f'Zmieniono {element} dla {player.name} na {value}')
  
@ACL.include
@arc.slash_command('kp-fabula', 'pokazuje KP postaci')
async def cmd_kp_fabula(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('imie postaci')] = None):
  player : FabulaPlayer
  
  if name:
    player = FABULA_PLAYER_DB.get_player_by_name(name)
    
    if player is None:
      return await ctx.respond(f"Nie ma postaci o imieniu \"{name}\" w bazie postaci **Fabula Ultima**")
  
  else:
    player = FABULA_PLAYER_DB.get_player(str(ctx.user.id))
    
    if player is None:
      return await ctx.respond("Nie posiadasz postaci w bazie postaci **Fabula Ultima**")

  await ctx.respond(
    tcr.discord.embed(
      tcr.Null,
      f'### Name: {player.name} \n Identity: {player.identity} \n Theme: {player.theme} \n Origin: {player.origin}\n Level: {player.clevel} \n Class: {print_list(player.character_class)} \n Skills: {print_dict(player.skill)}\n Stats: {print_dict(player.stats)}\n Current effects: {FabulaStatusEffectType.as_string(player.status)}\n',
      color=0xF0BFFF,
      footer='uwu',
      author={
        'name': f'KP - {player.name}',
        'icon': 'https://cdn.discordapp.com/attachments/866366097242325016/1209539245673422969/cute-anime-pfp-profile-pictures-girls-29.png?ex=65e74a34&is=65d4d534&hm=b76291968f902ca0ad92962354b9ab748f4d902bbd3ca229ed489dfd0de5bbca&',
      },
    )
  )
  
@ACL.include
@arc.slash_command('lvlup', 'zwiększa lvl postaci o 1')
async def cmd_lvlup(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('Imię postaci do lvlupa')] = None):
  owner : str
  player : tuple[str,FabulaPlayer]
  
  if name:
    pair = FABULA_PLAYER_DB.get_pair_by_value_attrs({"name" : name})
    if pair is None:
      return await ctx.respond(f"Nie ma postaci o imieniu \"{name}\" w bazie postaci **Fabula Ultima**")
    else:
      owner = pair[0]
      player = pair[1]
  else:
    owner = str(ctx.user.id)
    player = FABULA_PLAYER_DB.get_player(str(ctx.user.id))
    if player is None:
      return await ctx.respond("Nie posiadasz postaci w bazie postaci **Fabula Ultima**")
  
  player.clevel += 1
  player.stats["HP"] += 1
  player.stats["MP"] += 1
  FABULA_PLAYER_DB[owner] = player
  await ctx.respond(f'LVL UP! {player.name} ma lvl: {player.clevel}')
  
@ACL.include
@arc.slash_command('status-add', 'dodaje status do postaci')
async def cmd_status_add(ctx: arc.GatewayContext, statusy: arc.Option[str, arc.StrParams('status do dodania', choices=FabulaStatusEffectType.STATUSY.keys())], name: arc.Option[str, arc.StrParams('imie postaci')] = None):
  
  owner : str
  player : FabulaPlayer

  if name:
    pair = FABULA_PLAYER_DB.get_pair_by_value_attrs({"name" : name})
    
    if pair is None:
      return await ctx.respond(f"Nie ma postaci o imieniu \"{name}\" w bazie potaci **Fabula Ultima**")
    else:
      owner = pair[0]
      player = pair[1]
  else:
    owner = ctx.user.id
    player = FABULA_PLAYER_DB.get_value(owner)

    if player is None:
      return await ctx.respond("Nie posiadasz postaci w bazie postaci **Fabula Ultima**")

  statval = FabulaStatusEffectType.STATUSY[statusy]
  if(not player.has_status(statval)):
    player.status += statval
    
    managed_skills = get_corresponding_skills(statval)
    for managed_skill in managed_skills:
      player.skill[managed_skill] -= get_corresponding_debuff(managed_skill,statval)
    FABULA_PLAYER_DB[owner] = player
  
    await ctx.respond("Pomyślnie dodano status do postaci")
  else:
    await ctx.respond(f"Postać posiadała już status **{statusy}**")

@ACL.include
@arc.slash_command('status-del', 'dodaje status do postaci')
async def cmd_status_del(ctx: arc.GatewayContext,statusy: arc.Option[str, arc.StrParams('status do usuniecia', choices=FabulaStatusEffectType.STATUSY.keys())], name: arc.Option[str, arc.StrParams('imie postaci')] = None):

  owner : str
  player : FabulaPlayer

  if name:
    pair = FABULA_PLAYER_DB.get_pair_by_value_attrs({"name" : name})
    
    if pair is None:
      return await ctx.respond(f"Nie ma postaci o imieniu \"{name}\" w bazie potaci **Fabula Ultima**")
    else:
      owner = pair[0]
      player = pair[1]
  else:
    owner = ctx.user.id
    player = FABULA_PLAYER_DB.get_value(owner)

    if player is None:
      return await ctx.respond("Nie posiadasz postaci w bazie postaci **Fabula Ultima**")

  statval = FabulaStatusEffectType.STATUSY[statusy]
  if(not player.has_status(statval)):
    player.status -= statval
    
    managed_skills = get_corresponding_skills(statval)
    for managed_skill in managed_skills:
      player.skill[managed_skill] += get_corresponding_debuff(managed_skill,statval)
    FABULA_PLAYER_DB[owner] = player
  
    await ctx.respond("Pomyślnie dodano status do postaci")
  else:
    await ctx.respond(f"Postać posiadała już status **{statusy}**")