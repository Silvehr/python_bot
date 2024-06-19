from typing import Any


class FabulaStatusEffectType:
  STATUSY = {
    "none" : 0,
    "slow" : 1,
    "dazed" : 2,
    "weak" : 4,
    "shaken" : 8,
    "enraged" : 16,
    "poisoned" : 32
  }
  
  def __getattr__(self, name: str) -> Any:
    return self.STATUSY[name]