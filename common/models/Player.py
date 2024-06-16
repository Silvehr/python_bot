class Player:
    name : str
    
    def __init__(self, name) -> None:
        self.name = name
        
    def __repr__(self) -> str:
        return f'{self.character_name}'