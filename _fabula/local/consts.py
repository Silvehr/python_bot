from common.models.db.PlayerDB import PlayerDB
from common.models.db.CampaignDB import CampaignDB


STATUSY_FABULA = ['slow', 'dazed', 'enraged', 'weak', 'shaken', 'poisoned']

FABULA_PLAYER_DB = PlayerDB("fabula_players")
FABULA_CAMPAIGN_DB = CampaignDB("fabula_campaigns")