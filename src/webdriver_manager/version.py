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
        """Get the version of the installed Chrome browser."""
        system = platform.system().lower()
        
        if system == "linux":
            chrome_executables = [
                'google-chrome',
                'google-chrome-stable',
                'chromium',
                'chromium-browser'
            ]
            
            for executable in chrome_executables:
                try:
                    version = subprocess.check_output([executable, '--version'], 
                                                    stderr=subprocess.DEVNULL)
                    version = version.decode('utf-8')
                    match = re.search(ChromeVersion.VERSION_PATTERN, version)
                    if match:
                        return match.group(0)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
                    
            raise VersionError("Failed to detect Chrome version: Chrome not found")
            
        elif system == "darwin":
            try:
                process = subprocess.Popen(
                    ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                version = process.communicate()[0].decode('UTF-8')
                match = re.search(ChromeVersion.VERSION_PATTERN, version)
                if match:
                    return match.group(0)
                raise VersionError("Invalid Chrome version format")
            except Exception as e:
                raise VersionError(f"Failed to detect Chrome version: {str(e)}")
                
        elif system == "windows":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r'Software\Google\Chrome\BLBeacon')
                version, _ = winreg.QueryValueEx(key, 'version')
                match = re.search(ChromeVersion.VERSION_PATTERN, version)
                if match:
                    return match.group(0)
                raise VersionError("Invalid Chrome version format")
            except Exception as e:
                raise VersionError(f"Failed to detect Chrome version: {str(e)}")
                
        raise VersionError(f"Unsupported operating system: {system}")
    
    @staticmethod
    def get_major_version(version: str) -> int:
        """Extract the major version number from a version string."""
        try:
            return int(version.split('.')[0])
        except (IndexError, ValueError):
            raise VersionError(f"Invalid version format: {version}")
        return match.group(1)
    
    @staticmethod
    def is_compatible(chrome_version: str, driver_version: str) -> bool:
        """Check if ChromeDriver version is compatible with Chrome version."""
        try:
            chrome_major = ChromeVersion.get_major_version(chrome_version)
            driver_major = ChromeVersion.get_major_version(driver_version)
            return chrome_major == driver_major
        except VersionError:
            return False 