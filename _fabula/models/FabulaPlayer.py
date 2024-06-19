from common.models.Player import Player

class FabulaPlayer(Player):
  skill: dict[str, int]
  identity: str
  origin: str
  theme: str
  clevel: int
  stats: dict[str, int]
  character_class: list[str] = []
  status : int

  def __init__(
    self,
    character_name: str,
    identity: str,
    origin: str,
    theme: str,
    skill: dict[str, int],
    clevel: int,
    stats: dict[str, int],
    character_class: str,
    status: int,
  ):
    super().__init__(character_name)
    self.identity = identity
    self.origin = origin
    self.theme = theme
    self.skill = skill
    self.clevel = clevel
    self.stats = stats
    self.character_class = character_class
    self.status = status

  def __repr__(self) -> str:
    return f'{self.name}'
  
  def has_status(self, stat_val : int) -> bool:
    return self.status & stat_val