class Kata :
    def __init__(self, name, level, language, code):
        self.name = name; 
        self.level = level; 
        self.language = language; 
        self.code = code; 
    def __str__(self): 
        return "Nom: " + self.name + "\nNiveau: " + self.level + '\nLanguage: ' + self.language + '\nCode: ' + self.code; 
