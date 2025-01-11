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
from dotenv import load_dotenv, dotenv_values

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

config = dotenv_values()
mail_address = config.get('MAIL_ADDRESS')
password = config.get('PASSWORD')
local_repo_path = config.get('LOCAL_REPO_PATH')
file_name = config.get('KATA_FILE_NAME')
username = config.get('USERNAME')
push_step = config.get('PUSH_STEP')
actual_getted_katas = 0

class AuthenticationError(Exception):
    """Custom exception for authentication failures."""
    pass

def connection(max_attempts=3, delay=1):
    """
    Attempt to connect to Codewars with retry mechanism.
    
    Args:
        max_attempts (int): Maximum number of connection attempts
        delay (int): Delay in seconds between attempts
    
    Returns:
        bool: True if connection successful
    
    Raises:
        AuthenticationError: If authentication fails after all attempts
    """
    attempt = 1
    while attempt <= max_attempts:
        try:
            # Clear any existing input (in case of retry)
            email_field = gvars.web_driver.find_element('id', 'user_email')
            email_field.clear()
            email_field.send_keys(mail_address)
            
            password_field = gvars.web_driver.find_element('id', 'user_password')
            password_field.clear()
            password_field.send_keys(password)
            
            utils.get_element_ByXPATH('//button[@type="submit"]').click()
            
            # Wait for redirect and check if we're still on the login page
            time.sleep(1)  # Small delay to allow redirect
            if "sign_in" not in gvars.web_driver.current_url:
                logger.info("Authentication successful")
                return True
            
            logger.error(f"Authentication failed: Attempt {attempt}/{max_attempts}")
            
        except NoSuchElementException as e:
            logger.error(f"Element not found: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {str(e)}")
        
        attempt += 1
        if attempt <= max_attempts:
            time.sleep(delay)
    
    raise AuthenticationError(f"Authentication failed after {max_attempts} attempts")

def get_kata_code(element):
    return BeautifulSoup(element.find_element(By.TAG_NAME, 'code').get_attribute('innerHTML'), 'html.parser').get_text(); 

def get_kata_name(element): 
    return element.find_element(By.TAG_NAME, 'a').text; 

def get_kata_level(element): 
    return element.find_element(By.TAG_NAME, 'span').text;  

def get_kata_language(element):
    return element.find_element(By.TAG_NAME, 'code').get_attribute('data-language').lower(); 

def load_page(): 
      try:
        element = gvars.web_driver.find_element(By.CLASS_NAME, 'js-infinite-marker'); 
        gvars.web_driver.execute_script("arguments[0].scrollIntoView();", element); 
        return True; 
      except:
        return False; 

def save_kata(kata):
   toWrite = "# " + kata.name + ' [' + kata.level + '] #' + str(len(gvars.already_pushed_katas)) + '\n\n' + '```js\n' + kata.code + '\n```\n\n'; 
   file_management.add_kata_in_file(local_repo_path, file_name, toWrite); 
   commit(kata.name); 

def get_katas(): 
  global actual_getted_katas; 
  solutions_divs = gvars.web_driver.find_elements(By.CLASS_NAME, "list-item-solutions"); 
  for solution in solutions_divs: 
    kata_name = get_kata_name(solution.find_element(By.CLASS_NAME, 'item-title')); 
    if(actual_getted_katas >= int(push_step)): 
      return; 
    if (kata_name not in gvars.already_pushed_katas):
      kata_level = get_kata_level(solution.find_element(By.CLASS_NAME, 'item-title')); 
      kata_language = get_kata_language(solution.find_elements(By.CLASS_NAME, 'markdown')[0]); 
      kata_code = get_kata_code(solution.find_elements(By.CLASS_NAME, 'markdown')[0]); 
      if("kyu" in kata_level):
        kata = Kata(kata_name, kata_level, kata_language, kata_code); 
        gvars.completed_katas.append(kata); 
        gvars.already_pushed_katas.append(kata_name); 
        actual_getted_katas += 1; 
        save_kata(kata); 
  if(load_page() == True):
    get_katas(); 

def commit(kata_name):
  bashCommand = 'cd ' + local_repo_path + ' && git add . && git commit -m "docs(common): add \'' + kata_name + '\' kata"'; 
  os.system(bashCommand); 

def run():
    file_management.read_kata_file(local_repo_path, file_name)
    utils.start_browser_session()
    gvars.web_driver.get("https://www.codewars.com/users/sign_in")
    print("Connecting to your Codewars account...")
    try:
        connection()
        gvars.web_driver.get('https://www.codewars.com/users/' + username + '/completed_solutions')
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