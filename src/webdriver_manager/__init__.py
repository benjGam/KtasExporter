"""WebDriver management module."""

from webdriver_manager.chrome_manager import ChromeDriverManager
from webdriver_manager.exceptions import (
    DriverVersionError,
    DriverDownloadError,
    DriverInstallationError
)

__all__ = [
    'ChromeDriverManager',
    'DriverVersionError',
    'DriverDownloadError',
    'DriverInstallationError'
] 