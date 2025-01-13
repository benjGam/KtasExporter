import os
import platform
import logging
import subprocess
import shutil
from typing import Optional, Tuple
from .exceptions import DriverVersionError, DriverDownloadError, DriverInstallationError
from .version import ChromeVersion
from .system_utils import verify_npm_installation, verify_pnpm_installation, verify_yarn_installation

logger = logging.getLogger(__name__)

class ChromeDriverManager:
    """Manages ChromeDriver verification."""
    
    def __init__(self, install_path: Optional[str] = None):
        """Initialize ChromeDriver manager."""
        self.install_path = install_path or os.path.join(os.getcwd(), "chromedriver")
        self.system = platform.system().lower()
        self.executable = "chromedriver.exe" if self.system == "windows" else "chromedriver"
        self.driver_path = os.path.join(self.install_path, self.executable)
    
    def _get_package_manager_command(self) -> Tuple[str, str]:
        """
        Determine which package manager to use and return appropriate command.
        
        Returns:
            Tuple[str, str]: Package manager name and command to use
        
        Raises:
            DriverInstallationError: If no supported package manager is found
        """
        if verify_pnpm_installation():
            return "pnpm", "pnpm dlx"
        elif verify_yarn_installation():
            return "Yarn", "yarn dlx"
        elif verify_npm_installation():
            return "npm", "npx --yes"
        else:
            raise DriverInstallationError("No supported Node.js package manager (pnpm, yarn, or npm) found")
    
    def verify_driver(self) -> None:
        """Verify ChromeDriver exists and is executable."""
        if not os.path.exists(self.driver_path):
            raise DriverInstallationError(f"ChromeDriver not found at {self.driver_path}")
            
        if self.system != "windows":
            if not os.access(self.driver_path, os.X_OK):
                raise DriverInstallationError(f"ChromeDriver at {self.driver_path} is not executable")
                
        try:
            result = subprocess.run([self.driver_path, "--version"], capture_output=True, text=True)
            version = result.stdout.split()[1]
            logging.info(f"ChromeDriver version: {version}")
        except (subprocess.SubprocessError, IndexError) as e:
            raise DriverVersionError(f"Failed to get ChromeDriver version: {e}") 

    def update_if_needed(self) -> None:
        """Update ChromeDriver if needed."""
        try:
            self.verify_driver()
        except (DriverVersionError, DriverInstallationError):
            logger.info("ChromeDriver needs to be updated")
            self._download_driver()
            self.verify_driver()

    def _download_driver(self) -> None:
        """Download ChromeDriver using available package manager."""
        try:
            # Determine which package manager to use
            pkg_manager, cmd_prefix = self._get_package_manager_command()
            logger.info(f"Using {pkg_manager} to download ChromeDriver")
            
            chrome_version = ChromeVersion.get_chrome_version()
            major_version = ChromeVersion.get_major_version(chrome_version)
            
            logger.info(f"Downloading ChromeDriver for Chrome version {major_version}")
            
            # Create temporary directory for download
            temp_dir = os.path.join(self.install_path, "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Use package manager with full path and appropriate options
            cmd = f"{cmd_prefix} @puppeteer/browsers install chromedriver@{major_version}"
            
            # Execute command in temporary directory
            result = subprocess.run(cmd.split(), 
                                 capture_output=True, 
                                 text=True,
                                 cwd=temp_dir)
            
            if result.returncode != 0:
                raise DriverDownloadError(f"Failed to download ChromeDriver: {result.stderr}")
            
            # Find downloaded chromedriver path
            chrome_path = None
            for root, _, files in os.walk(temp_dir):
                if self.executable in files:
                    chrome_path = os.path.join(root, self.executable)
                    break
            
            if not chrome_path:
                raise DriverDownloadError("ChromeDriver executable not found after download")
                
            # Set permissions on Linux/Mac
            if self.system != "windows":
                os.chmod(chrome_path, 0o755)
            
            # Remove old chromedriver if exists
            if os.path.exists(self.driver_path):
                os.remove(self.driver_path)
            
            # Copy executable to installation directory
            shutil.copy2(chrome_path, self.driver_path)
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
                
            logger.info("ChromeDriver downloaded successfully")
            
        except Exception as e:
            raise DriverDownloadError(f"Failed to download ChromeDriver: {e}")