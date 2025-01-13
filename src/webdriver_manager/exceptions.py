"""WebDriver manager exceptions."""

class DriverVersionError(Exception):
    """Raised when there is an error with the driver version."""
    pass

class DriverDownloadError(Exception):
    """Raised when there is an error downloading the driver."""
    pass

class DriverInstallationError(Exception):
    """Raised when there is an error installing the driver."""
    pass 