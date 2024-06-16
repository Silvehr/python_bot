import shelve
from pathlib import *
import os

class ShelveDB:
    DEFAULT_DB_FOLDER = "./db"
    
    _open : bool
    _dir_path : Path
    _db_path : Path
    _shelf : shelve.Shelf
    
    def __init__(self, db_name : str):
        self._dir_path = Path(f"{self.DEFAULT_DB_FOLDER}/{db_name}")
        self._db_path = Path(f"{str(self._dir_path)}/{db_name}")
        
        if not Path.exists(Path(self.DEFAULT_DB_FOLDER).absolute()):
            os.mkdir(self.DEFAULT_DB_FOLDER)
        
        if not Path.exists(self._dir_path):
            print(str(self._dir_path.absolute()))
            os.mkdir(str(self._dir_path.absolute()))
        
        self._shelf = shelve.open(str(self._db_path.absolute()))
        self._open = True
    
    def __del__(self):
        self._shelf.sync()
        self._shelf.close()
        self._open = False
        
    def __getitem__(self, key : str):
        key = str(key)
        
        try:
            if not self._open:
                self._shelf = shelve.open(str(self._dir_path))
                self._open = True
            
            return self._shelf[key]
        except Exception as e:
            self._shelf.sync()
            self._shelf.close()
            raise Exception from e
        
    def __setitem__(self, key, value):
        key = str(key)
        
        try:
            if not self._open:
                self._shelf = shelve.open(str(self._dir_path))
                self._open = True
            
            self._shelf[key] = value
        except Exception as e:
            self._shelf.sync()
            self._shelf.close()
            self._open = False
            raise Exception from e
        
    def __enter__(self):
        if not self._open:
            self._shelf = shelve.open(str(self._dir_path))
            self._open = True
            
        return self
    
    def __exit__(self):
        self._shelf.sync()
        self._shelf.close()
        self._open = False