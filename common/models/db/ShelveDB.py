import shelve
from pathlib import *
import os
from typing import Any

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
        
        if not self._open:
            self._shelf = shelve.open(str(self._dir_path))
            self._open = True
            
        return self._shelf[key]
        
    def __setitem__(self, key, value):
        key = str(key)
        
        if not self._open:
            self._shelf = shelve.open(str(self._dir_path))
            self._open = True
            
        self._shelf[key] = value
        
    def __delitem__(self, key):
        key = str(key)

        if not self._open:
            self._shelf = shelve.open(str(self._dir_path))
            self._open = True
            
        self._shelf.pop(key)                
        
    def __enter__(self):
        if not self._open:
            self._shelf = shelve.open(str(self._dir_path))
            self._open = True
            
        return self
    
    def __exit__(self):
        self._shelf.sync()
        self._shelf.close()
        self._open = False
        
    def __contains__(self, key : str):
        return key in self._shelf
    
    def get_value(self, key) -> Any | None:
        return self._shelf.get(key)
    
    def items(self) -> dict:
        return self._shelf.items()
    
    #
    # if found:
    #   returns the first key value pair for which ALL attributes listed in attrs take passed values
    # else:
    #   returns None
    #
    def get_pair_by_value_attrs(self, attrs : dict[str, Any]) -> tuple | None:
        for pair in self._shelf.items():
            for attr in attrs.items():
                if getattr(pair[1], attr[0]) != attr[1]:
                    break
                return pair
        
        return None
    
    def get_value_by_attrs(self, attrs : dict[str, Any]) -> Any | None:
        for value in self._shelf.values():
            for attr in attrs.items():
                if getattr(value, attr[0]) != attr[1]:
                    break
                return value
            
        return None