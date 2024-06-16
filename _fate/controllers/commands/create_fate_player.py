from _fate.local.consts import FATE_PLAYER_DB
from _fate.models.FatePlayer import FatePlayer

from common.dsc import *

@ACL.include
@arc.slash_command('create-fate-player', 'dodaje gracza fate')
async def cmd_addplayerfate(
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
  skill = dict([x.split(' ') for x in skill])
  skill = {x: int(y) for x, y in skill.items()}
  fate_player = FatePlayer(name, aspect, skill)
  FATE_PLAYER_DB[str(user.id)] = fate_player
  await ctx.respond(f'Pomyślnie stworzono gracza {name}')