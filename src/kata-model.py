class Kata:
    """
    Represents a Codewars kata solution.
    
    Attributes:
        name (str): The name of the kata
        level (str): The difficulty level of the kata (e.g. '6 kyu')
        language (str): The programming language used
        code (str): The solution code
    """
    
    def __init__(self, name: str, level: str, language: str, code: str) -> None:
        """
        Initialize a new Kata instance.
        
        Args:
            name: The name of the kata
            level: The difficulty level
            language: The programming language used
            code: The solution code
        """
        self.name = name
        self.level = level
        self.language = language
        self.code = code
    
    def __str__(self) -> str:
        """Return a string representation of the Kata."""
        return f"Name: {self.name}\nLevel: {self.level}\nLanguage: {self.language}\nCode: {self.code}"
