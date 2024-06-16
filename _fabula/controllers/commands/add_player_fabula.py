from common.dsc import *
from _fabula.models.FabulaPlayer import *
from _fabula.local.consts import *

@ACL.include
@arc.slash_command('add-player-fabula', 'dodaje gracza fabula')
async def cmd_addplayerfabula(
  ctx: arc.GatewayContext,
  name: arc.Option[str, arc.StrParams('imie postaci')],
  skill: arc.Option[str, arc.StrParams('umiejki twojej postaci')],
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
  skill = skill.split(',')
  skill = dict([x.split(' ') for x in skill])
  skill = {x: int(y) for x, y in skill.items()}
  stats = stats.split(',')
  stats = dict([x.split(' ') for x in stats])
  stats = {x: int(y) for x, y in stats.items()}
  character_class = character_class.split(',')
  fabula_player = FabulaPlayer(name, identity, origin, theme, skill, clevel, stats, character_class)
  FABULA_PLAYER_DB[str(user.id)] = fabula_player
  await ctx.respond(f'Pomyślnie stworzono gracza {name}')