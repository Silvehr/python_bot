from .ShelveDB import ShelveDB
from common.models.Player import Player

class PlayerDB(ShelveDB):
    def __init__(self, db_name: str):
        super().__init__(db_name)
        
    def get_player_by_name(self, name: str) -> Player:
        return [player for player in self._shelf.values() if player.name.lower() == name.lower()][0]
    
    def get_player_by_attr_value(self, attr_name : str, attr_value) -> Player:
        for i in range(len(self._shelf.keys())):
            if getattr(self._shelf[i], attr_name) == attr_value:
                return self._shelf[i]
        
        raise KeyError()
    
    def __getitem__(self, key : str) -> Player:
        return super().__getitem__(key)
        
    def __setitem__(self, key, value : Player):
        super().__setitem__(key, value)