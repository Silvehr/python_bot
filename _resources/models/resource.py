class Resource:
    full_name : str
    is_file : bool
    url : str
    
    def __init__(self, full_name : str, url : str, is_file : bool) -> None:
        self.full_name = full_name
        self.url = url
        self.is_file = is_file
    