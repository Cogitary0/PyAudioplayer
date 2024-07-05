from toml import (load as tLoad, 
                  dump as tDump)


class Settings:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load()


    def load(self) -> dict[str]:
        with open(self.filename, 'r') as f:
            data = tLoad(f)
        return data


    def save(self) -> None:
        with open(self.filename, 'w') as f:
            tDump(self.data, f)


    def get(self, key:str) -> dict[str]:
        return self.data.get(key)
    
    
    def set(self, key:str, value:int|str):
        self.data[key] = value
        self.save()
        return 
    

class Language:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.parse_file()
        
    def parse_file(self):
        with open(self.filename, 'r') as lang_file:
            return tLoad.load(lang_file)
        
    
 
    
    
