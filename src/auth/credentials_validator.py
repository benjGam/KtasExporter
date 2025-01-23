import logging
from typing import Optional, Tuple
from selenium.common.exceptions import NoSuchElementException
from .user_credentials import Credentials
from .exceptions import AuthenticationError, ValidationError
from .security_utils import SensitiveDataMasker

logger = logging.getLogger(__name__)

class CredentialsValidator:
    """Handles validation and authentication of credentials."""
    
    def __init__(self, web_driver, max_attempts: int = 3, delay: int = 1):
        """
        Initialize validator with web driver and retry settings.
        
        Args:
            web_driver: Selenium WebDriver instance
            max_attempts: Maximum number of authentication attempts
            delay: Delay between attempts in seconds
        """
        self.web_driver = web_driver
        self.max_attempts = max_attempts
        self.delay = delay
    
    def authenticate(self, credentials: Credentials) -> bool:
        """
        Attempt to authenticate with provided credentials.
        
        Args:
            credentials: User credentials
            
        Returns:
            bool: True if authentication successful
            
        Raises:
            AuthenticationError: If authentication fails after all attempts
        """
        masked_email, masked_pass = SensitiveDataMasker.mask_credentials(
            credentials.email,
            credentials.password
        )
        logger.info(f"Attempting authentication for {masked_email}")
        
        attempt = 1
        while attempt <= self.max_attempts:
            try:
                if self._try_authentication(credentials):
                    logger.info("Authentication successful")
                    return True
                
                logger.error(f"Authentication failed: Attempt {attempt}/{self.max_attempts}")
                
            except NoSuchElementException as e:
                logger.error(f"Element not found: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error during authentication: {str(e)}")
            
            attempt += 1
            if attempt <= self.max_attempts:
                logger.info(f"Waiting {self.delay} seconds before next attempt...")
                import time
                time.sleep(self.delay)
        
        raise AuthenticationError(f"Authentication failed after {self.max_attempts} attempts")
    
    def _try_authentication(self, credentials: Credentials) -> bool:
        """
        Single authentication attempt.
        
        Args:
            credentials: User credentials
            
        Returns:
            bool: True if authentication successful
        """
        # Clear any existing input
        email_field = self.web_driver.find_element('id', 'user_email')
        email_field.clear()
        email_field.send_keys(credentials.email)
        
        password_field = self.web_driver.find_element('id', 'user_password')
        password_field.clear()
        password_field.send_keys(credentials.password)
        
        # Find and click submit button
        submit_button = self.web_driver.find_element('xpath', '//button[@type="submit"]')
        submit_button.click()
        
        # Wait for redirect and check if successful
        import time
        time.sleep(1)  # Small delay to allow redirect
        return "sign_in" not in self.web_driver.current_url 