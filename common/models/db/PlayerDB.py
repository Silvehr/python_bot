from .ShelveDB import ShelveDB
from common.models.Player import Player
from typing import Any

class PlayerDB(ShelveDB):
    def __init__(self, db_name: str):
        super().__init__(db_name)
    
    def __getitem__(self, key : str) -> Player:
        return super().__getitem__(key) #may raise Exception
        
    def __setitem__(self, key, value : Player):
        super().__setitem__(key, value)
        
    def get_player_by_name(self, name: str) -> Player | None:
        return super().get_value_by_attrs({"name": name})
    
    def get_player_by_attrs(self, attrs : dict[str, Any]) -> Player | None:
        return super().get_value_by_attrs(attrs)
        
    def get_player(self, key) -> Player | None:
        return self._shelf.get(key)
    
    def items(self) -> dict[Any, Player]:
        return self._shelf.items()