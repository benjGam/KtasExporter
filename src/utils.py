import gvars
import os
import platform
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from Kata import Kata
from selenium.webdriver.chrome.service import Service
from webdriver_manager import ChromeDriverManager

logger = logging.getLogger(__name__)

# Selenium utils

def start_browser_session():
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Initialize ChromeDriver manager
        manager = ChromeDriverManager(os.path.dirname(__file__))
        manager.update_if_needed()
        
        # Create service with managed ChromeDriver
        service = Service(executable_path=manager.executable_path)
        gvars.web_driver = webdriver.Chrome(options=options, service=service)
        logger.info("Browser session started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start browser session: {str(e)}")
        exit(1)

def element_exists(element): 
    return element != None

def element_isInteractable(element):
    if(element_exists(element)):
        return element.is_displayed() and element.is_enabled()
    return None

def page_has_loaded(): 
    if(element_exists(gvars.web_driver.find_element(By.TAG_NAME, 'html'))):
        return True
    return False

def element_isHidden(element):
    return element.get_attribute('hidden') != None

def get_element_ByXPATH(toXPath):
    if(gvars.web_driver == None):
        return None
    return gvars.web_driver.find_element(By.XPATH, toXPath)

def wait_until_page_loaded(): 
    try: 
        while(not element_isHidden(get_element_ByXPATH('//div[@class="loading page fadeIn"]'))):
            time.sleep(0.000001)
    except: 
        pass
    try:
        while(not element_isHidden(get_element_ByXPATH('//div[@class="loading page"]'))):
            time.sleep(0.000001)
    except:
        pass

def wait_until_element_become_interactable(element):
    while(not element_isInteractable(element)):
        time.sleep(0.001)

# Bots utils

def clear_console(): 
    if(platform.system() == 'Linux'):
        os.system('clear')
    elif(platform.system() == 'Windows'): 
        os.system('cls')