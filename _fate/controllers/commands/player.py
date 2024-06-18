from common.dsc import *
from common.functions import *
import tcrutils as tcr

from _fate.local import *
from _fate.models import *

@ACL.include
@arc.slash_command('kp-fate', 'karta postaci fate')
async def cmd_kp_fate(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('Imie postaci')] = None):
  autid = ctx.author.id
  cname = name
  if cname is None:
    try:
      player = FATE_PLAYER_DB[str(autid)]
    except KeyError:
      return await ctx.respond('nie jesteś w bazie danych')
  else:
    try:
      player = FATE_PLAYER_DB.get_player_by_name(name)
    except IndexError:
      return await ctx.respond('nie ma takiej postaci')
  await ctx.respond(
    tcr.discord.embed(
      tcr.Null,
      f'### Name: {player.character_name} \n### Aspect: \n{'\n'.join(player.aspect)} \n### Skills: \n{'\n'.join(f'{x}: {y}' for x, y in player.skill.items())} \n',
      color=0xF0BFFF,
      footer='uwu',
      author={
        'name': f'KP - {player.character_name}',
        'icon': 'https://cdn.discordapp.com/attachments/866366097242325016/1209539245673422969/cute-anime-pfp-profile-pictures-girls-29.png?ex=65e74a34&is=65d4d534&hm=b76291968f902ca0ad92962354b9ab748f4d902bbd3ca229ed489dfd0de5bbca&',
      },
    )
  )
  
@ACL.include
@arc.slash_command('del-fate-player', 'usuwa gracza fate')
async def cmd_del_fate_player(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('imie postaci do usunięcia')]):
  try:
    v = FATE_PLAYER_DB.get_player_by_name(name)
    for key, value in FATE_PLAYER_DB.items():
      if value == v:
        del FATE_PLAYER_DB[key]
        break
  except (KeyError, IndexError):
    return await ctx.respond('nie ma takiej postaci chyba dobrze')
  return await ctx.respond(f'pomyślnie usunięto gracza {name}')

@ACL.include
@arc.slash_command('create-fate-player', 'dodaje gracza fate')
async def cmd_create_fate_player(
  ctx: arc.GatewayContext,
  name: arc.Option[str, arc.StrParams('imie postaci')],
  aspect: arc.Option[str, arc.StrParams('aspekty postaci rozdzielone ,')],
  skill: arc.Option[str, arc.StrParams('umiejki postaci np: wiedza 4, walka 3')],
  user: arc.Option[hikari.User, arc.UserParams('Gracz do postaci')] = None,
):
  if user is None:
    user = ctx.user
  aspect = aspect.split(',')
  skill = skill.split(',')
  dict_skill : dict[str,int] = {}
  
  for x in skill:
    x = x.strip().split(" ")
    dict_skill[x[0]] = int(x[1])
    
  fate_player = FatePlayer(name, aspect, dict_skill)
  FATE_PLAYER_DB[str(user.id)] = fate_player
  await ctx.respond(f'Pomyślnie stworzono gracza {name}')