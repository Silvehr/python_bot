from common.models.db.PlayerDB import PlayerDB
from common.models.db.CampaignDB import CampaignDB

STATY_FATE = ['budowa', 'empatia', 'kontakty', 'kradziez', 'oszustwo', 'prowadzenie', 'prowokacja', 'relacje', 'mechanika', 'spostrzegawczosc', 'sprawnosc', 'strzelanie', 'sledztwo', 'ukrywanie', 'walka', 'wiedza', 'wola', 'zasoby']

FATE_PLAYER_DB = PlayerDB("fate_players")
FATE_CAMPAIGN_DB = CampaignDB("fate_campaigns")