import json
import os

class Preferences:

    def __init__(self, filename):
        self.filename = filename
        self.datas = {}

    def load_preferences(self):

        if not os.path.exists(self.filename):

            raise Exception(f"Fichier de paramètres '${self.filename}' introuvable.")
            
        with open(self.filename, "r", encoding="utf8") as file:

            self.datas = json.load(file)
        
        file.close()
    
    
    def write_preferences(self):
       
        with open(self.filename, "w+", encoding="utf8") as file:

            json.dump(self.datas, file, ensure_ascii=False, indent=4)
        
        file.close()

    
    def get_value(self, key, default_value):

        if self.datas.keys().__contains__(key):
            return self.datas[key]
        else:
            return default_value
        
    def update_preference(self, key, value):

        self.datas[key] = value
        self.write_preferences()
            


