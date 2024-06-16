from common.dsc import *
from common.functions import *

from _fate.local.consts import *

import tcrutils as tcr

@ACL.include
@arc.slash_command('kp_fate', 'karta postaci fate')
async def cmd_kpfate(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('Imie postaci')] = None):
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