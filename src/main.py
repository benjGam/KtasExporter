import os
import platform
import time
import utils
import gvars
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv, dotenv_values

load_dotenv()

config = dotenv_values(); 
mail_address = config.get('MAIL_ADDRESS'); 
password = config.get('PASSWORD'); 
branch = config.get('BRANCH_TO_PUSH'); 
local_repo_path = config.get('LOCAL_REPO_PATH'); 
file_name = config.get('KATA_FILE_NAME'); 
push_step = config.get('PUSH_STEP'); 

total_completed_katas = 0; 
completed_katas = {}; 

class Kata :
    def __init__(self, name, level, language, code):
        self.name = name; 
        self.level = level; 
        self.language = language; 
        self.code = code; 

def connection(): 
  gvars.web_driver.find_element('id', 'user_email').send_keys(mail_address); 
  gvars.web_driver.find_element('id', 'user_password').send_keys(password); 
  utils.get_element_ByXPATH('//button[@type="submit"]').click(); 

def get_katas(): 
  solutions_divs = gvars.web_driver.find_elements(By.CLASS_NAME, "list-item-solutions"); 
  for solution in solutions_divs: 
    for element in solution.find_elements(By.XPATH, '*'): 
      kata_level = get_kata_level(element); 
      kata_name = get_kata_name(element); 
      kata_language = ""; 
      kata_code = ""; 
    print(get_kata_name(element)); 

def get_kata_name(element): 
  if(element.get_attribute('class') == 'item-title'):
    return element.find_element(By.TAG_NAME, 'a').text; 

def get_kata_level(element): 
  if(element.get_attribute('class') == 'item-title'): # Getting katas level
    return element.find_element(By.TAG_NAME, 'span').text;  

def run(): 
  utils.start_browser_session(); 
  gvars.web_driver.get("https://www.codewars.com/users/sign_in"); 
  connection(); 
  gvars.web_driver.get('https://www.codewars.com/users/Mecopi/completed_solutions'); 
  get_katas(); 

run(); 