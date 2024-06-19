from common.dsc import *
from _fabula.models import *
from _fabula.local import *

from common.functions import *

import tcrutils as tcr

@ACL.include
@arc.slash_command('create-fabula-player', 'tworzy gracza fabula')
async def cmd_create_fabula_player(
  ctx: arc.GatewayContext,
  name: arc.Option[str, arc.StrParams('imie postaci')],
  attributes: arc.Option[str, arc.StrParams('atrybuty twojej postaci (DEX, INS, MP, WLP)')],
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
    dict_attributes[x[0]] = int(x[1])
  
  stats = stats.split(',')
  dict_stats = {}
  
  for x in stats:
    x = x.strip().split(" ")
    dict_stats[x[0]] = int(x[1])
  
  character_class = character_class.split(',')
  fabula_player = FabulaPlayer(name, identity, origin, theme, dict_attributes, clevel, dict_stats, character_class, 0)
  FABULA_PLAYER_DB[str(user.id)] = fabula_player
  
  await ctx.respond(f'Pomyślnie stworzono gracza {name}')
  
@ACL.include
@arc.slash_command('del-fabula-player', 'usuwa gracza fabula')
async def cmd_del_fabula_player(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('imie postaci do usunięcia')]):
  try:
    v = FABULA_PLAYER_DB.get_player_by_name(name)
    for key, value in FABULA_PLAYER_DB.items():
      if value == v:
        del FABULA_PLAYER_DB[key]
        break
  except (KeyError, IndexError):
    return await ctx.respond('nie ma takiej postaci chyba dobrze')
  return await ctx.respond(f'pomyślnie usunięto gracza {name}')

@ACL.include
@arc.slash_command('edit-fabula-character', 'edytuje konkretny element postaci w systemie fabula')
async def cmd_edit_fabula_character(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('Imie postaci')],element: arc.Option[str, arc.StrParams('element do edycji', choices=list(FabulaPlayer.__annotations__))], value: arc.Option[str, arc.StrParams('nowa zawartosc')]):
  character = FABULA_PLAYER_DB[name]
  character.__setattr__(element, value)
  FABULA_PLAYER_DB[name] = character
  await ctx.respond(f'Zmieniono {element} dla {name} na {value}')
  
@ACL.include
@arc.slash_command('kp-fabula', 'pokazuje KP postaci')
async def cmd_kp_fabula(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('imie postaci')] = None):
  autid = ctx.author.id
  cname = name

  if cname is None:
    try:
      player = FABULA_PLAYER_DB[str(autid)]
    except KeyError:
      return await ctx.respond('nie jesteś w bazie danych')
  else:
    try:
      player = FABULA_PLAYER_DB.get_player_by_name(cname)
    except IndexError:
      return await ctx.respond('nie ma takiej postaci')

  await ctx.respond(
    tcr.discord.embed(
      tcr.Null,
      f'### Name: {player.name} \n Identity: {player.identity} \n Theme: {player.theme} \n Origin: {player.origin}\n Level: {player.clevel} \n Class: {print_list(player.character_class)} \n Skills: {print_dict(player.skill)}\n Stats: {print_dict(player.stats)}\n Current effects: {player.status}\n',
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
async def cmd_lvlup(ctx: arc.GatewayContext, user: arc.Option[hikari.User, arc.UserParams('Postać do lvlupa')] = None):
  if user is None:
    user = ctx.user
  character = FABULA_PLAYER_DB[str(user.id)]
  character.clevel += 1
  character.stats["HP"] += 1
  character.stats["MP"] += 1
  FABULA_PLAYER_DB[str(user.id)] = character
  await ctx.respond(f'LVL UP! {character.name} ma lvl: {character.clevel}')
  
@ACL.include
@arc.slash_command('status-add', 'dodaje status do postaci')
async def cmd_status_add(ctx: arc.GatewayContext,name: arc.Option[str, arc.StrParams('imie postaci')], statusy: arc.Option[str, arc.StrParams('status do dodania', choices=FabulaStatusEffectType.STATUSY.keys())]):
  character : FabulaPlayer
  name = name.lower()
  for i in FABULA_PLAYER_DB._shelf.keys():
    if(FABULA_PLAYER_DB[i].name.lower() == name):
      character = FABULA_PLAYER_DB[i]
      break
  addval = FabulaStatusEffectType.STATUSY[statusy]
  if(not (character.status & addval)):
    character.status += addval
  managed_skill = get_corresponding_skill(statusy)
  character.skill[managed_skill] -= get_corresponding_debuff(managed_skill, statusy)
  FABULA_PLAYER_DB[name] = character
  ctx.respond("Pomyślnie dodano status do postaci")

@ACL.include
@arc.slash_command('status-del', 'dodaje status do postaci')
async def cmd_status_del(ctx: arc.GatewayContext,name: arc.Option[str, arc.StrParams('imie postaci')],statusy: arc.Option[str, arc.StrParams('status do usuniecia', choices=FabulaStatusEffectType.STATUSY.keys())]):
  character = FABULA_PLAYER_DB[name]
  addval = FabulaStatusEffectType.STATUSY[statusy]
  if(character.status & addval):
    character.status -= addval
  managed_skill = get_corresponding_skill(statusy)
  character.skill[managed_skill] += get_corresponding_debuff(managed_skill, statusy)
  FABULA_PLAYER_DB[name] = character
  ctx.respond("Pomyślnie usunięto status do postaci")