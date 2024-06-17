from common.dsc import *
from common.functions import *

from _fabula.models.FabulaPlayer import *
from _fabula.local.consts import *

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