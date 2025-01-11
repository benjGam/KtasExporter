import re
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

class CredentialsValidationError(Exception):
    """Exception raised for credentials validation errors."""
    pass

class CredentialsValidator:
    """Handles validation of credentials and environment variables."""
    
    # Minimum requirements
    MIN_PASSWORD_LENGTH = 8
    REQUIRED_ENV_VARS = ['MAIL_ADDRESS', 'PASSWORD', 'USERNAME', 'LOCAL_REPO_PATH', 'KATA_FILE_NAME']
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: The email address to validate
            
        Returns:
            bool: True if email is valid
            
        Raises:
            CredentialsValidationError: If email format is invalid
        """
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email or not email_pattern.match(email):
            raise CredentialsValidationError("Invalid email format")
        return True
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate password requirements.
        
        Args:
            password: The password to validate
            
        Returns:
            bool: True if password meets requirements
            
        Raises:
            CredentialsValidationError: If password requirements are not met
        """
        if not password or len(password) < CredentialsValidator.MIN_PASSWORD_LENGTH:
            raise CredentialsValidationError(
                f"Password must be at least {CredentialsValidator.MIN_PASSWORD_LENGTH} characters long"
            )
        return True
    
    @staticmethod
    def validate_env_vars(config: Dict[str, str]) -> bool:
        """
        Validate presence and format of required environment variables.
        
        Args:
            config: Dictionary containing environment variables
            
        Returns:
            bool: True if all required variables are present and valid
            
        Raises:
            CredentialsValidationError: If any required variable is missing or invalid
        """
        missing_vars = [var for var in CredentialsValidator.REQUIRED_ENV_VARS if not config.get(var)]
        if missing_vars:
            raise CredentialsValidationError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
            
        # Validate specific variables
        CredentialsValidator.validate_email(config['MAIL_ADDRESS'])
        CredentialsValidator.validate_password(config['PASSWORD'])
        
        return True
    
    @staticmethod
    def mask_sensitive_data(data: str) -> str:
        """
        Mask sensitive data for logging purposes.
        
        Args:
            data: The sensitive data to mask
            
        Returns:
            str: Masked version of the data
        """
        if not data:
            return ""
        return data[:2] + "*" * (len(data) - 4) + data[-2:] if len(data) > 4 else "*" * len(data)
    
    @staticmethod
    def validate_credentials(config: Dict[str, str]) -> Tuple[bool, Optional[str]]:
        """
        Main method to validate all credentials and configuration.
        
        Args:
            config: Dictionary containing all configuration variables
            
        Returns:
            Tuple[bool, Optional[str]]: (Success status, Error message if any)
        """
        try:
            CredentialsValidator.validate_env_vars(config)
            logger.info("Credentials validation successful")
            return True, None
        except CredentialsValidationError as e:
            error_msg = f"Credentials validation failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error during credentials validation: {str(e)}"
            logger.error(error_msg)
            return False, error_msg 