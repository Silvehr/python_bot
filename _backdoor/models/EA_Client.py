class EA_Client:
    user_id : str
    enabled : bool
    
    def __init__(self, user_id : str) -> None:
       self.user_id = user_id
       self.enabled = False
       
    def enable(self):
        self.enabled = True
        
    def disable(self):
        self.enabled = False