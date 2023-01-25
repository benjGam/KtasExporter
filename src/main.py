import os
import platform
import time
import utils
import file_management
import gvars
import subprocess 
from Kata import Kata
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
local_repo_path = config.get('LOCAL_REPO_PATH'); 
file_name = config.get('KATA_FILE_NAME'); 
push_step = config.get('PUSH_STEP'); 
actual_getted_katas = 0; 


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

def load_page(): 
      try:
        element = gvars.web_driver.find_element(By.CLASS_NAME, 'js-infinite-marker'); 
        gvars.web_driver.execute_script("arguments[0].scrollIntoView();", element); 
        return True; 
      except:
        return False; 

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
        gvars.completed_katas.append(Kata(kata_name, kata_level, kata_language, kata_code)); 
        gvars.already_pushed_katas.append(kata_name); 
        actual_getted_katas += 1; 
  if(load_page() == True):
    get_katas(); 

def commit():
  bashCommand = 'cd ' + local_repo_path + ' && git add ' + file_name + ' && git commit -m "docs(common): add kata"'; 
  os.system(bashCommand); 

def run(): 
  file_management.read_kata_file(local_repo_path, file_name); 
  utils.start_browser_session(); 
  gvars.web_driver.get("https://www.codewars.com/users/sign_in"); 
  connection(); 
  gvars.web_driver.get('https://www.codewars.com/users/Mecopi/completed_solutions'); 
  get_katas(); 
  i = len(gvars.already_pushed_katas) - int(push_step) + 1; 
  for kata in gvars.completed_katas:
    toWrite = "# " + kata.name + " ||| #" + str(i) + ' [' + kata.level + ']\n' + '```js\n' + kata.code + '\n```\n'; 
    file_management.add_kata_in_file(local_repo_path, file_name, toWrite); 
    i += 1; 
    commit(); 
  print('Vos ' + push_step + ' ont étés commités'); 


run(); 