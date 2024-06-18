from typing import Any


class FabulaStatusEffectType:
    STATUSY = {
        "none": 0,
        "slow": 1,
        "dazed": 2,
        "enraged": 4,
        "weak": 8,
        "shaken": 16,
        "poisoned": 32
    }
  
    def __getattr__(self, name: str):
        if name in self.STATUSY:
            return self.STATUSY[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
  
    @classmethod
    def as_string(cls, status_value):
        if status_value == 0:
            return "none"
        
        result : str = ""
        
        for i in cls.STATUSY.items():
            if status_value & i[1]:
                result += i[0]+ " "
        
        return result