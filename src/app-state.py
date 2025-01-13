"""Module managing global application state."""

from typing import List, Optional
from selenium import webdriver

class ApplicationState:
    """
    Manages global application state.
    
    This class provides a centralized way to manage the application's global state,
    including the WebDriver instance and kata tracking.
    """
    
    def __init__(self):
        """Initialize application state."""
        self._web_driver: Optional[webdriver.Chrome] = None
        self._completed_katas: List[str] = []
        self._pushed_katas: List[str] = []
        self._different_file_depending_on_language: bool = False
    
    @property
    def different_file_depending_on_language(self) -> bool:
        """Get the language-based file separation setting."""
        return self._different_file_depending_on_language
    
    @different_file_depending_on_language.setter
    def different_file_depending_on_language(self, value: bool) -> None:
        """Set the language-based file separation setting."""
        self._different_file_depending_on_language = value
    
    @property
    def web_driver(self) -> Optional[webdriver.Chrome]:
        """Get the current WebDriver instance."""
        return self._web_driver
    
    @web_driver.setter
    def web_driver(self, driver: webdriver.Chrome) -> None:
        """Set the WebDriver instance."""
        self._web_driver = driver
    
    @property
    def completed_katas(self) -> List[str]:
        """Get list of completed katas."""
        return self._completed_katas
    
    def add_completed_kata(self, kata_name: str) -> None:
        """Add a kata to completed list."""
        if kata_name not in self._completed_katas:
            self._completed_katas.append(kata_name)
    
    @property
    def pushed_katas(self) -> List[str]:
        """Get list of pushed katas."""
        return self._pushed_katas
    
    def add_pushed_kata(self, kata_name: str) -> None:
        """Add a kata to pushed list."""
        if kata_name not in self._pushed_katas:
            self._pushed_katas.append(kata_name)
    
    def is_kata_pushed(self, kata_name: str) -> bool:
        """Check if a kata has been pushed."""
        return kata_name in self._pushed_katas
    
    def cleanup(self) -> None:
        """Cleanup application state."""
        if self._web_driver:
            self._web_driver.quit()
            self._web_driver = None

# Global instance
app_state = ApplicationState() 