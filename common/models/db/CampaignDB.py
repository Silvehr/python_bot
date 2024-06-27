from .ShelveDB import ShelveDB
from common.models.Campaign import Campaign 
from typing import Any

class CampaignDB(ShelveDB):
    def __init__(self, db_name: str):
        super().__init__(db_name)
    
    def __getitem__(self, key : str) -> Campaign:
        return super().__getitem__(key)
        
    def __setitem__(self, key, value : Campaign):
        super().__setitem__(key, value)
        
    def get_campaign_by_name(self, name: str) -> Campaign | None:
        return self.get_campaign_by_attrs({"name": name})
    
    def get_campaign_by_attrs(self, attrs : dict[str, Any]) -> Campaign | None:
        
        result = super().get_value_by_attrs(attrs)
        
        if result is None:
            return None
        else:
            return result[1]
        
    def get_campaign(self, key) -> Campaign | None:
        return super().get_value(key=key)
    
    def items(self) -> dict[Any, Campaign]:
        return self._shelf.items()