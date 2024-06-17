from common.dsc import *

from _fabula.local.consts import *
from _fabula.local.functions import *
from _fabula.models.FabulaPlayer import FabulaPlayer
from _fabula.models.FabulaStatusEffectType import FabulaStatusEffectType

import inspect

@ACL.include
@arc.slash_command('status-del', 'dodaje status do postaci')
async def cmd_status_del(ctx: arc.GatewayContext,name: arc.Option[str, arc.StrParams('imie postaci')],statusy: arc.Option[str, arc.StrParams('status do usuniecia', choices=STATUSY_FABULA)]):
  character = FABULA_PLAYER_DB[name]
  addval = FabulaStatusEffectType.__getattribute__(statusy)
  if(character.status & addval):
    character.status -= addval
  managed_skill = get_corresponding_skill(statusy)
  character.skill[managed_skill] += get_corresponding_debuff(managed_skill, statusy)
  FABULA_PLAYER_DB[name] = character
  ctx.respond("Pomyślnie usunięto status do postaci")