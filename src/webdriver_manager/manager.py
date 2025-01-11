import os
import platform
import requests
import zipfile
import logging
import subprocess
from typing import Optional
from .exceptions import DownloadError, InstallationError, VersionError
from .version import ChromeVersion

logger = logging.getLogger(__name__)

class ChromeDriverManager:
    """Manages ChromeDriver installation and updates."""
    
    CHROMEDRIVER_URL = "https://chromedriver.storage.googleapis.com"
    
    def __init__(self, install_path: str):
        """
        Initialize ChromeDriver manager.
        
        Args:
            install_path: Path where ChromeDriver should be installed
        """
        self.install_path = install_path
        self.system = platform.system().lower()
        self._setup_paths()
    
    def _setup_paths(self) -> None:
        """Setup necessary paths and create directories if needed."""
        os.makedirs(self.install_path, exist_ok=True)
        
        # Set platform-specific executable name
        if self.system == "windows":
            self.executable = "chromedriver.exe"
        else:
            self.executable = "chromedriver"
            
        self.executable_path = os.path.join(self.install_path, self.executable)
    
    def get_compatible_version(self, chrome_version: str) -> str:
        """
        Get compatible ChromeDriver version for given Chrome version.
        
        Args:
            chrome_version: Chrome version string
            
        Returns:
            str: Compatible ChromeDriver version
            
        Raises:
            DownloadError: If version information cannot be retrieved
        """
        try:
            # Get list of available versions
            response = requests.get(f"{self.CHROMEDRIVER_URL}/LATEST_RELEASE_{ChromeVersion.get_major_version(chrome_version)}")
            if response.status_code != 200:
                raise DownloadError("Failed to get ChromeDriver version information")
            return response.text.strip()
        except requests.RequestException as e:
            raise DownloadError(f"Failed to get ChromeDriver version: {str(e)}")
    
    def download_driver(self, version: str) -> str:
        """
        Download ChromeDriver for current platform.
        
        Args:
            version: ChromeDriver version to download
            
        Returns:
            str: Path to downloaded file
            
        Raises:
            DownloadError: If download fails
        """
        # Determine platform-specific download URL
        if self.system == "linux":
            platform_name = "linux64"
        elif self.system == "darwin":
            platform_name = "mac64"  # Add arm64 support if needed
        elif self.system == "windows":
            platform_name = "win32"
        else:
            raise DownloadError(f"Unsupported platform: {self.system}")
            
        download_url = f"{self.CHROMEDRIVER_URL}/{version}/chromedriver_{platform_name}.zip"
        
        try:
            # Download the file
            response = requests.get(download_url, stream=True)
            if response.status_code != 200:
                raise DownloadError(f"Failed to download ChromeDriver: HTTP {response.status_code}")
                
            # Save to temporary file
            zip_path = os.path.join(self.install_path, "chromedriver.zip")
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return zip_path
            
        except requests.RequestException as e:
            raise DownloadError(f"Failed to download ChromeDriver: {str(e)}")
    
    def install_driver(self, zip_path: str) -> None:
        """
        Install ChromeDriver from downloaded zip file.
        
        Args:
            zip_path: Path to downloaded zip file
            
        Raises:
            InstallationError: If installation fails
        """
        try:
            # Extract the executable
            with zipfile.ZipFile(zip_path) as z:
                z.extract(self.executable, self.install_path)
                
            # Make executable on Unix systems
            if self.system != "windows":
                os.chmod(self.executable_path, 0o755)
                
            # Clean up
            os.remove(zip_path)
            
        except (zipfile.BadZipFile, OSError) as e:
            raise InstallationError(f"Failed to install ChromeDriver: {str(e)}")
    
    def update_if_needed(self) -> bool:
        """
        Check if ChromeDriver needs update and perform it if necessary.
        
        Returns:
            bool: True if update was performed
            
        Raises:
            VersionError: If Chrome version cannot be detected
            DownloadError: If download fails
            InstallationError: If installation fails
        """
        chrome_version = ChromeVersion.get_chrome_version()
        logger.info(f"Detected Chrome version: {chrome_version}")
        
        try:
            driver_version = subprocess.check_output([self.executable_path, "--version"]).decode().split()[1]
            logger.info(f"Current ChromeDriver version: {driver_version}")
            
            if ChromeVersion.is_compatible(chrome_version, driver_version):
                logger.info("ChromeDriver is up to date")
                return False
                
        except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
            logger.info("ChromeDriver not found or version check failed")
        
        # Get compatible version and perform update
        compatible_version = self.get_compatible_version(chrome_version)
        logger.info(f"Downloading ChromeDriver version: {compatible_version}")
        
        zip_path = self.download_driver(compatible_version)
        self.install_driver(zip_path)
        
        logger.info("ChromeDriver updated successfully")
        return True 