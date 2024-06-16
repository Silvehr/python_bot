from _fabula.models.FabulaPlayer import *
from _fabula.models.FabulaStatusEffectType import *
from _fabula.local.consts import FABULA_PLAYER_DB

def get_corresponding_debuff(skill_name :str, status_value : int):
  status_value = status_value.upper()
  if(skill_name == "DEX"):
    return (status_value & FabulaStatusEffectType.slow) + (status_value & FabulaStatusEffectType.enraged)
  elif(skill_name == "INS"):
    return (status_value & FabulaStatusEffectType.dazed) + (status_value & FabulaStatusEffectType.enraged)
  elif(skill_name == "MIG"):
    return (status_value & FabulaStatusEffectType.weak) + (status_value & FabulaStatusEffectType.posioned)
  elif(skill_name == "WLP"):
    return (status_value & FabulaStatusEffectType.shaken) + (status_value & FabulaStatusEffectType.posioned)
  else:
    raise Exception(f"Da faq is skill \"{skill_name}\"")
  
  
def get_corresponding_skill(status_value : int):
  if((status_value & FabulaStatusEffectType.slow) or (status_value & FabulaStatusEffectType.enraged)):
    return "DEX"
  elif((status_value & FabulaStatusEffectType.dazed) or (status_value & FabulaStatusEffectType.enraged)):
    return "INS"
  elif((status_value & FabulaStatusEffectType.weak) or (status_value & FabulaStatusEffectType.posioned)):
    return "MIG"
  elif((status_value & FabulaStatusEffectType.shaken) or (status_value & FabulaStatusEffectType.posioned)):
    return "WLP"
  else:
    raise Exception(f'Da faq is this status "{status_value}"')
    
  