import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def check_command_exists(command: str) -> bool:
    """
    Check if a command exists in the system PATH.
    
    Args:
        command: The command to check
        
    Returns:
        bool: True if command exists, False otherwise
    """
    try:
        subprocess.run([command, '--version'], 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE, 
                     check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def verify_npm_installation() -> bool:
    """
    Verify if npm is installed on the system.
    
    Returns:
        bool: True if npm is installed, False otherwise
    """
    if not check_command_exists('npm'):
        logger.error("npm is not installed. Please install Node.js and npm to use this feature.")
        return False
    return True 