from common.dsc.gateways import *
from common.models.Campaign import *
from common.models.Campaign import CampaignSystem

class CyberpunkCampaign (Campaign):
    def __init__(self, name: str, universe: str, gms: list[str], players: list[str], roles: list[int]):
        super().__init__(name, CampaignSystem.CYBERPUNK, universe, gms, players, roles)