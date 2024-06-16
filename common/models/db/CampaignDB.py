from .ShelveDB import ShelveDB
from common.models.Campaign import Campaign 

class CampaignDB(ShelveDB):
    def __init__(self, db_name: str):
        super().__init__(db_name)
        
    def get_campaign_by_name(self, name: str) -> Campaign:
        return [campaign for campaign in self._shelf.values() if campaign.name == name.lower()][0]
    
    def get_campaign_by_attr_value(self, attr_name : str, attr_value) -> Campaign:
        for i in range(len(self._shelf.keys())):
            if getattr(self._shelf[i], attr_name) == attr_value:
                return self._shelf[i]
        
        raise KeyError()
    
    def __getitem__(self, key : str) -> Campaign:
        return super().__getitem__(key)
        
    def __setitem__(self, key, value : Campaign):
        super().__setitem__(key, value)