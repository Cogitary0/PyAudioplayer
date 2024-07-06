from toml import (load as tLoad, 
                  dump as tDump)

# COUNT_WORDS = 8

class Settings:
    def __init__(self, filename:str):
        self.__filename = filename
        self.__data = self.load()


    def load(self) -> dict[str]:
        with open(self.__filename, 'r') as f:
            data = tLoad(f)
        return data


    def save(self) -> None:
        with open(self.__filename, 'w') as f:
            tDump(self.__data, f)


    def get(self, key:str) -> dict[str]:
        return self.__data.get(key)
    
    
    def set(self, key:str, value:int|str):
        self.__data[key] = value
        self.save()
        return 
    

class Language:
    def __init__(self, filename:str, language:str):
        self.__filename = filename
        self.__language = language
        self.__data = self.get_file()
        
        
    def get_file(self):
        with open(self.__filename, 'r', encoding='utf-8') as lang_file:
            return tLoad(lang_file)
        
        
    def get(self, word:str) -> str:
        return self.__data.get(self.__language)[word]
    
    
    def get_lang(self) -> list[str]:
        # all_langs = [lang for lang in self.get_file().keys()]
        # all_words = [ [code_word for code_word in self.get_file()[all_langs[num_lang]].keys()] for num_lang in range(len(all_langs)) ]
        return [lang for lang in self.get_file().keys()]
    
    