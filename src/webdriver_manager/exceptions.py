class ChromeDriverError(Exception):
    """Base exception for ChromeDriver related errors."""
    pass

class VersionError(ChromeDriverError):
    """Exception raised for version incompatibility issues."""
    pass

class DownloadError(ChromeDriverError):
    """Exception raised when ChromeDriver download fails."""
    pass

class InstallationError(ChromeDriverError):
    """Exception raised when ChromeDriver installation fails."""
    pass 