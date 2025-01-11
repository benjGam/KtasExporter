import os
import platform
import time
import utils
import file_management
import gvars
import logging
from Kata import Kata
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from config import Configuration
from auth.exceptions import ConfigurationError
from auth import (
    Credentials,
    CredentialsValidator,
    AuthenticationError,
    ValidationError
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Load and validate configuration
    config = Configuration()
    
    # Create credentials object
    credentials = Credentials(
        email=config.mail_address,
        password=config.password,
        username=config.username
    )
    
    # Initialize other configuration values
    local_repo_path = config.local_repo_path
    file_name = config.kata_file_name
    push_step = config.push_step
    actual_getted_katas = 0
    
except (ConfigurationError, ValidationError) as e:
    logger.error(f"Configuration error: {str(e)}")
    print("Please check your .env file and try again.")
    exit(1)

def get_kata_code(element):
    return BeautifulSoup(element.find_element(By.TAG_NAME, 'code').get_attribute('innerHTML'), 'html.parser').get_text()

def get_kata_name(element): 
    return element.find_element(By.TAG_NAME, 'a').text

def get_kata_level(element): 
    return element.find_element(By.TAG_NAME, 'span').text

def get_kata_language(element):
    return element.find_element(By.TAG_NAME, 'code').get_attribute('data-language').lower()

def load_page(): 
    try:
        element = gvars.web_driver.find_element(By.CLASS_NAME, 'js-infinite-marker')
        gvars.web_driver.execute_script("arguments[0].scrollIntoView();", element)
        return True
    except:
        return False

def save_kata(kata):
    toWrite = "# " + kata.name + ' [' + kata.level + '] #' + str(len(gvars.already_pushed_katas)) + '\n\n' + '```js\n' + kata.code + '\n```\n\n'
    file_management.add_kata_in_file(local_repo_path, file_name, toWrite)
    commit(kata.name)

def get_katas(): 
    global actual_getted_katas
    solutions_divs = gvars.web_driver.find_elements(By.CLASS_NAME, "list-item-solutions")
    for solution in solutions_divs: 
        kata_name = get_kata_name(solution.find_element(By.CLASS_NAME, 'item-title'))
        if actual_getted_katas >= push_step:
            return
        if kata_name not in gvars.already_pushed_katas:
            kata_level = get_kata_level(solution.find_element(By.CLASS_NAME, 'item-title'))
            kata_language = get_kata_language(solution.find_elements(By.CLASS_NAME, 'markdown')[0])
            kata_code = get_kata_code(solution.find_elements(By.CLASS_NAME, 'markdown')[0])
            if "kyu" in kata_level:
                kata = Kata(kata_name, kata_level, kata_language, kata_code)
                gvars.completed_katas.append(kata)
                gvars.already_pushed_katas.append(kata_name)
                actual_getted_katas += 1
                save_kata(kata)
    if load_page():
        get_katas()

def commit(kata_name):
    bashCommand = 'cd ' + local_repo_path + ' && git add . && git commit -m "docs(common): add \'' + kata_name + '\' kata"'
    os.system(bashCommand)

def run():
    file_management.read_kata_file(local_repo_path, file_name)
    utils.start_browser_session()
    gvars.web_driver.get("https://www.codewars.com/users/sign_in")
    print("Connecting to your Codewars account...")
    
    try:
        # Initialize validator with web driver
        validator = CredentialsValidator(gvars.web_driver)
        
        # Attempt authentication
        validator.authenticate(credentials)
        
        # Navigate to completed solutions
        gvars.web_driver.get(f'https://www.codewars.com/users/{credentials.username}/completed_solutions')
        print("Getting completed katas...")
        get_katas()
        
    except AuthenticationError as e:
        logger.error(str(e))
        print("Failed to authenticate. Please check your credentials and try again.")
        exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        print("An error occurred. Check the logs for more details.")
        exit(1)

run() 