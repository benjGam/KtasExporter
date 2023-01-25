import os
import platform
import time
import utils
import gvars
from bs4 import BeautifulSoup
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
completed_katas = []; 

class Kata :
    def __init__(self, name, level, language, code):
        self.name = name; 
        self.level = level; 
        self.language = language; 
        self.code = code; 
    def __str__(self): 
        return "Nom: " + self.name + "\nNiveau: " + self.level + '\nLanguage: ' + self.language + '\nCode: ' + self.code; 


def connection(): 
  gvars.web_driver.find_element('id', 'user_email').send_keys(mail_address); 
  gvars.web_driver.find_element('id', 'user_password').send_keys(password); 
  utils.get_element_ByXPATH('//button[@type="submit"]').click(); 

def get_kata_code(element):
    return BeautifulSoup(element.find_element(By.TAG_NAME, 'code').get_attribute('innerHTML'), 'html.parser').get_text(); 

def get_kata_name(element): 
    return element.find_element(By.TAG_NAME, 'a').text; 

def get_kata_level(element): 
    return element.find_element(By.TAG_NAME, 'span').text;  

def get_kata_language(element):
    return element.find_element(By.TAG_NAME, 'code').get_attribute('data-language').lower(); 

def get_katas(): 
  solutions_divs = gvars.web_driver.find_elements(By.CLASS_NAME, "list-item-solutions"); 
  for solution in solutions_divs: 
    kata_level = get_kata_level(solution.find_element(By.CLASS_NAME, 'item-title')); 
    kata_name = get_kata_name(solution.find_element(By.CLASS_NAME, 'item-title')); 
    kata_language = get_kata_language(solution.find_elements(By.CLASS_NAME, 'markdown')[0]); 
    kata_code = get_kata_code(solution.find_elements(By.CLASS_NAME, 'markdown')[0]); 
    completed_katas.append(Kata(kata_name, kata_level, kata_language, kata_code)); 
  
  for kata in completed_katas:
    print(kata); 


def run(): 
  utils.start_browser_session(); 
  gvars.web_driver.get("https://www.codewars.com/users/sign_in"); 
  connection(); 
  gvars.web_driver.get('https://www.codewars.com/users/Mecopi/completed_solutions'); 
  get_katas(); 

run(); 