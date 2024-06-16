from common.models.Campaign import Campaign, CampaignSystem

class FabulaCampaign(Campaign):
    def __init__(self, name: str, universe: str, gms: list[str], players: list[str], roles: list[int]):
        super().__init__(name, CampaignSystem.FABULA, universe, gms, players, roles)