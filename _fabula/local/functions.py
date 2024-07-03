from _fabula.models import *

def get_corresponding_debuff(skill_name :str, status_value : int):
  skill_name = skill_name.upper()
  if(skill_name == "DEX"):
    return 2 * ((status_value & FabulaStatusEffectType.STATUSY["slow"] == status_value) + (status_value & FabulaStatusEffectType.STATUSY["enraged"] == status_value))
  elif(skill_name == "INS"):
    return 2 * ((status_value & FabulaStatusEffectType.STATUSY["dazed"] == status_value) + (status_value & FabulaStatusEffectType.STATUSY["enraged"] == status_value))
  elif(skill_name == "MIG"):
    return 2 * ((status_value & FabulaStatusEffectType.STATUSY["weak"] == status_value) + (status_value & FabulaStatusEffectType.STATUSY["poisoned"] == status_value))
  elif(skill_name == "WLP"):
    return 2 * ((status_value & FabulaStatusEffectType.STATUSY["shaken"] == status_value) + (status_value & FabulaStatusEffectType.STATUSY["poisoned"] == status_value))
  else:
    raise Exception(f"Da faq is skill \"{skill_name}\"")
  
  
def get_corresponding_skills(status_value : int) -> list[str]:
  
  result : list[str] = list()
  
  if((status_value & FabulaStatusEffectType.STATUSY["slow"]) or (status_value & FabulaStatusEffectType.STATUSY["enraged"])):
    result.append("DEX")
  if((status_value & FabulaStatusEffectType.STATUSY["dazed"]) or (status_value & FabulaStatusEffectType.STATUSY["enraged"])):
    result.append("INS")
  if((status_value & FabulaStatusEffectType.STATUSY["weak"]) or (status_value & FabulaStatusEffectType.STATUSY["poisoned"])):
    result.append("MIG")
  if((status_value & FabulaStatusEffectType.STATUSY["shaken"]) or (status_value & FabulaStatusEffectType.STATUSY["poisoned"])):
    result.append("WLP")
    
  return result
    
  