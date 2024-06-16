from _fate.local.consts import *
from _fate.local.functions import *
from common.functions import *

from common.dsc import *


@ACL.include
@arc.slash_command('del_fate_player', 'usuwa gracza fate')
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