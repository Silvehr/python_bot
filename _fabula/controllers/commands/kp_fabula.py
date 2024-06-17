from common.dsc import *
from common.functions import *

from _fabula.local.consts import *
from _fabula.local.functions import *

import random as rng
import tcrutils as tcr

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
      f'### Name: {player.character_name} \n Identity: {player.identity} \n Theme: {player.theme} \n Origin: {player.origin}\n Level: {player.clevel} \n Class: {print_list(player.character_class)} \n Skills: {print_dict(player.skill)}\n Stats: {print_dict(player.stats)}\n Current effects: {player.status}\n',
      color=0xF0BFFF,
      footer='uwu',
      author={
        'name': f'KP - {player.character_name}',
        'icon': 'https://cdn.discordapp.com/attachments/866366097242325016/1209539245673422969/cute-anime-pfp-profile-pictures-girls-29.png?ex=65e74a34&is=65d4d534&hm=b76291968f902ca0ad92962354b9ab748f4d902bbd3ca229ed489dfd0de5bbca&',
      },
    )
  )