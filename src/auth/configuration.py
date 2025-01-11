import os
import logging
from typing import Dict, Optional
from dotenv import load_dotenv, dotenv_values
from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)

class Configuration:
    """Manages application configuration and environment variables."""
    
    REQUIRED_VARS = [
        'MAIL_ADDRESS',
        'PASSWORD',
        'USERNAME',
        'LOCAL_REPO_PATH',
        'KATA_FILE_NAME'
    ]
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration from environment file.
        
        Args:
            env_file: Path to .env file (optional)
        """
        self._config: Dict[str, str] = {}
        self._load_configuration(env_file)
        
    def _load_configuration(self, env_file: Optional[str]) -> None:
        """Load configuration from environment file."""
        if env_file and not os.path.exists(env_file):
            raise ConfigurationError(f"Environment file not found: {env_file}")
        
        load_dotenv(env_file)
        self._config = dotenv_values(env_file)
        self._validate_configuration()
    
    def _validate_configuration(self) -> None:
        """Validate presence of required environment variables."""
        missing_vars = [var for var in self.REQUIRED_VARS if not self._config.get(var)]
        if missing_vars:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def __getitem__(self, key: str) -> str:
        """
        Get configuration value using dictionary syntax.
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value
            
        Raises:
            ConfigurationError: If key not found
        """
        if key not in self._config:
            raise ConfigurationError(f"Configuration key not found: {key}")
        return self._config[key]
    
    @property
    def mail_address(self) -> str:
        """Get mail address."""
        return self['MAIL_ADDRESS']
    
    @property
    def password(self) -> str:
        """Get password."""
        return self['PASSWORD']
    
    @property
    def username(self) -> str:
        """Get username."""
        return self['USERNAME']
    
    @property
    def local_repo_path(self) -> str:
        """Get local repository path."""
        return self['LOCAL_REPO_PATH']
    
    @property
    def kata_file_name(self) -> str:
        """Get kata file name."""
        return self['KATA_FILE_NAME']
    
    @property
    def push_step(self) -> int:
        """Get push step with default value."""
        return int(self.get('PUSH_STEP', '5')) 