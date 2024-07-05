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
    def __init__(self, filename, language):
        self.filename = filename
        self.language = language
        self.data = self.get_file()
        
        
    def get_file(self) -> dict:
        with open(self.filename, 'r', encoding='utf-8') as lang_file:
            return tLoad(lang_file)
        
        
    def get(self, word:str) -> str:
        return self.data.get(self.language)[word]
    
    

        
    
 
    
    
