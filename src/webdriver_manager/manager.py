import os
import platform
import logging
import subprocess
from typing import Optional
from .exceptions import ChromeDriverError

logger = logging.getLogger(__name__)

class ChromeDriverManager:
    """Manages ChromeDriver verification."""
    
    def __init__(self, install_path: Optional[str] = None):
        """Initialize ChromeDriver manager."""
        self.install_path = install_path or os.path.join(os.getcwd(), "chromedriver")
        self.system = platform.system().lower()
        self.executable = "chromedriver.exe" if self.system == "windows" else "chromedriver"
        self.driver_path = os.path.join(self.install_path, self.executable)
    
    def verify_driver(self) -> None:
        """Verify ChromeDriver exists and is executable."""
        if not os.path.exists(self.driver_path):
            raise ChromeDriverError(f"ChromeDriver not found at {self.driver_path}")
            
        if self.system != "windows":
            if not os.access(self.driver_path, os.X_OK):
                raise ChromeDriverError(f"ChromeDriver at {self.driver_path} is not executable")
                
        try:
            result = subprocess.run([self.driver_path, "--version"], capture_output=True, text=True)
            version = result.stdout.split()[1]
            logging.info(f"ChromeDriver version: {version}")
        except (subprocess.SubprocessError, IndexError) as e:
            raise ChromeDriverError(f"Failed to get ChromeDriver version: {e}") 

    def update_if_needed(self) -> None:
        """Update ChromeDriver if needed."""
        try:
            self.verify_driver()
        except ChromeDriverError:
            logger.info("ChromeDriver needs to be updated")
            self._download_driver()
            self.verify_driver()

    def _download_driver(self) -> None:
        """Download ChromeDriver using npm."""
        try:
            chrome_version = ChromeVersion.get_chrome_version()
            major_version = ChromeVersion.get_major_version(chrome_version)
            
            logger.info(f"Downloading ChromeDriver for Chrome version {major_version}")
            cmd = f"npx @puppeteer/browsers install chromedriver@{major_version}"
            
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode != 0:
                raise ChromeDriverError(f"Failed to download ChromeDriver: {result.stderr}")
                
            logger.info("ChromeDriver downloaded successfully")
            
        except Exception as e:
            raise ChromeDriverError(f"Failed to download ChromeDriver: {e}") 