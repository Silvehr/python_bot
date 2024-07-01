from abc import ABC, abstractmethod

class Logger:
    
    @classmethod
    @abstractmethod
    async def log_event(self,message: str):
        ...
    
    @classmethod
    @abstractmethod
    async def log_warning(self, warning : str):
        ...
    
    @classmethod
    @abstractmethod   
    async def log_error(self, error : Exception | str):
        ...