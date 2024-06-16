from common.dsc import *

from _fabula.local.consts import *
from _fabula.local.functions import *
from _fabula.models.FabulaPlayer import FabulaPlayer
from _fabula.models.FabulaStatusEffectType import FabulaStatusEffectType

import inspect


@ACL.include
@arc.slash_command('status-add', 'dodaje status do postaci')
async def cmd_status_add(ctx: arc.GatewayContext,name: arc.Option[str, arc.StrParams('imie postaci')], statusy: arc.Option[str, arc.StrParams('status do dodania', choices=list(inspect.getmembers(FabulaStatusEffectType)))]):
  character : FabulaPlayer
  name = name.lower()
  for i in FABULA_PLAYER_DB.keys():
    if(FABULA_PLAYER_DB[i].character_name.lower() == name):
      character = FABULA_PLAYER_DB[i]
      break
  addval = FabulaStatusEffectType.__getattribute__(statusy)
  if(not (character.status & addval)):
    character.status += addval
  managed_skill = get_corresponding_skill(statusy)
  character.skill[managed_skill] -= get_corresponding_debuff(managed_skill, statusy)
  FABULA_PLAYER_DB[name] = character