from enum import Enum

class CampaignSystem(Enum):
  FATE = 'fate'
  FABULA = 'fabula'

class Campaign:
  name: str
  system: CampaignSystem
  universe: str
  gms: list[str]
  players: list[str]
  roles: list[int]

  def __init__(self, name: str, system: CampaignSystem, universe: str, gms: list[str], players: list[str], roles: list[int]):
    self.name = name
    self.system = system
    self.universe = universe
    self.gms = gms
    self.players = players
    self.roles = roles