import re
import subprocess
import platform
from typing import Optional
from .exceptions import VersionError

class ChromeVersion:
    """Handles Chrome version detection and comparison."""
    
    VERSION_PATTERN = re.compile(r'(\d+)\.(\d+)\.(\d+)\.(\d+)')
    
    @staticmethod
    def get_chrome_version() -> str:
        """ 
        Get installed Chrome version.
        
        Returns:
            str: Chrome version (e.g., "94.0.4606.81")
            
        Raises:
            VersionError: If Chrome version cannot be detected
        """
        system = platform.system().lower()
        
        try:
            if system == "linux":
                output = subprocess.check_output(["google-chrome", "--version"])
                version = output.decode().strip().split()[-1]
            elif system == "darwin":  # MacOS
                output = subprocess.check_output(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"])
                version = output.decode().strip().split()[-1]
            elif system == "windows":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                version = winreg.QueryValueEx(key, "version")[0]
            else:
                raise VersionError(f"Unsupported operating system: {system}")
                
            if not ChromeVersion.VERSION_PATTERN.match(version):
                raise VersionError(f"Invalid Chrome version format: {version}")
                
            return version
            
        except (subprocess.CalledProcessError, FileNotFoundError, ImportError) as e:
            raise VersionError(f"Failed to detect Chrome version: {str(e)}")
    
    @staticmethod
    def get_major_version(version: str) -> str:
        """
        Extract major version number.
        
        Args:
            version: Full version string
            
        Returns:
            str: Major version number
        """
        match = ChromeVersion.VERSION_PATTERN.match(version)
        if not match:
            raise VersionError(f"Invalid version format: {version}")
        return match.group(1)
    
    @staticmethod
    def is_compatible(chrome_version: str, driver_version: str) -> bool:
        """
        Check if ChromeDriver version is compatible with Chrome version.
        
        Args:
            chrome_version: Chrome version
            driver_version: ChromeDriver version
            
        Returns:
            bool: True if versions are compatible
        """
        return ChromeVersion.get_major_version(chrome_version) == ChromeVersion.get_major_version(driver_version) 