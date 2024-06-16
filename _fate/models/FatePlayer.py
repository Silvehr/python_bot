class FatePlayer:
  character_name: str
  aspect: list[str]
  skill: dict[str, int]
  

  def __init__(self, character_name, aspect: list[str], skill: dict[str, int]):
    self.character_name = character_name
    self.aspect = aspect
    self.skill = skill

  def __repr__(self) -> str:
    return f'{self.character_name}'