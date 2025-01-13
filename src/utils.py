"""Utility functions for browser automation and system operations."""

import os
import platform
import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager import ChromeDriverManager
import gvars

logger = logging.getLogger(__name__)

def start_browser_session() -> None:
    """Initialize and configure Chrome WebDriver session."""
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        manager = ChromeDriverManager(os.path.dirname(__file__))
        manager.update_if_needed()
        
        service = webdriver.chrome.service.Service(executable_path=manager.driver_path)
        gvars.web_driver = webdriver.Chrome(options=options, service=service)
        logger.info("Browser session started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start browser session: {str(e)}")
        exit(1)

def wait_for_element(by: By, value: str, timeout: int = 10) -> Optional[webdriver.remote.webelement.WebElement]:
    """
    Wait for element to be present and visible.
    
    Args:
        by: Selenium By locator
        value: Locator value
        timeout: Maximum wait time in seconds
        
    Returns:
        WebElement if found, None otherwise
    """
    try:
        wait = WebDriverWait(gvars.web_driver, timeout)
        return wait.until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException:
        return None

def wait_for_page_load(timeout: int = 10) -> bool:
    """
    Wait for page to finish loading.
    
    Args:
        timeout: Maximum wait time in seconds
        
    Returns:
        bool: True if page loaded, False otherwise
    """
    try:
        wait = WebDriverWait(gvars.web_driver, timeout)
        wait.until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        return True
    except TimeoutException:
        return False

def clear_console() -> None:
    """Clear console based on operating system."""
    os.system('clear' if platform.system() == 'Linux' else 'cls')