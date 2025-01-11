from dataclasses import dataclass
from typing import Optional
import re
from .exceptions import ValidationError

@dataclass
class Credentials:
    """Encapsulates user credentials with validation."""
    
    email: str
    password: str
    username: Optional[str] = None
    
    MIN_PASSWORD_LENGTH = 8
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __post_init__(self):
        """Validate credentials after initialization."""
        self.validate()
    
    def validate(self) -> None:
        """
        Validate credentials format.
        
        Raises:
            ValidationError: If credentials format is invalid
        """
        self._validate_email()
        self._validate_password()
    
    def _validate_email(self) -> None:
        """
        Validate email format.
        
        Raises:
            ValidationError: If email format is invalid
        """
        if not self.email or not self.EMAIL_PATTERN.match(self.email):
            raise ValidationError("Invalid email format")
    
    def _validate_password(self) -> None:
        """
        Validate password requirements.
        
        Raises:
            ValidationError: If password requirements are not met
        """
        if not self.password or len(self.password) < self.MIN_PASSWORD_LENGTH:
            raise ValidationError(
                f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters long"
            )
    
    def __str__(self) -> str:
        """Return string representation with masked password."""
        return f"Credentials(email='{self.email}', username='{self.username}', password='****')" 