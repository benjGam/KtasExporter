import gvars
import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Selenium utils

def start_browser_session():
    options = webdriver.ChromeOptions(); 
    options.add_argument("no-sandbox"); 
    options.add_argument("--disable-gpu"); 
    options.add_argument("--disable-dev-shm-usage"); 
    options.add_experimental_option("detach", True); 
    try:
        if(platform.system() == 'Linux'):
            gvars.web_driver = webdriver.Chrome(os.path.dirname(__file__) + "/chromedriver", options=options); 
        elif(platform.system() == 'Windows'): 
            gvars.web_driver = webdriver.Chrome(os.path.dirname(__file__) + "/chromedriver.exe", options=options); 
        else:
            return None; 
    except Exception as e:
        print('Une erreur est survenue, verifiez que les drivers Chrome sont bien présents dans le dossier'); 
        print('Ou assurez-vous de l\'installation de Chrome.'); 
        print('Si le problème persiste, ouvrez une issue sur le repo du bot avec le message d\'erreur suivant : ' + str(e));  
        exit(); 

def element_exists(element): 
    return element != None; 

def element_isInteractable(element):
    if(element_exists(element)):
        return element.is_displayed() and element.is_enabled(); 
    return None; 

def page_has_loaded(): 
    if(element_exists(gvars.web_driver.find_element(By.TAG_NAME, 'html'))):
        return True; 
    return False; 

def element_isHidden(element):
    return element.get_attribute('hidden') != None; 

def get_element_ByXPATH(toXPath):
    global web_driver; 
    if(gvars.web_driver == None):
        return None; 
    return gvars.web_driver.find_element(By.XPATH, toXPath); 

def wait_until_page_loaded(): 
    try: 
        while(not element_isHidden(get_element_ByXPATH('//div[@class="loading page fadeIn"]'))):
            time.sleep(0.1); 
    except: 
        pass; 
    try:
        while(not element_isHidden(get_element_ByXPATH('//div[@class="loading page"]'))):
            time.sleep(0.1); 
    except:
        pass; 
    time.sleep(0.5); 

def wait_until_element_become_interactable(element):
    while(not element_isInteractable(element)):
        time.sleep(0.1); 
    time.sleep(0.5); 

# Bots utils

def clear_console(): 
    if(platform.system() == 'Linux'):
        os.system('clear'); 
    elif(platform.system() == 'Windows'): 
        os.system('cls'); 

def define_configuration(text, key, default_value, possibilities={}, convert=False):
    user_entry = input(text); 
    if(user_entry == ''):
        gvars.configuration[key] = default_value; 
        return; 
    for possibility in possibilities:
        if(user_entry.lower() == possibility):
            gvars.configuration[key] = user_entry; 
            return; 
        gvars.configuration[key] = default_value; 
    else: 
        if(convert):
            try:
                gvars.configuration[key] = type(default_value)(user_entry); 
            except:
                gvars.configuration[key] = default_value; 
        else: 
            gvars.configuration[key] = user_entry; 
        
def check_config_file():
    for key in gvars.NORMAL_CONFIGURATION:
        if(gvars.configuration[key] == None):
            gvars.configuration[key] == gvars.NORMAL_CONFIGURATION[key]; 
            continue; 
        if(type(gvars.configuration[key]) != type(gvars.NORMAL_CONFIGURATION[key])): 
            gvars.configuration[key] == gvars.NORMAL_CONFIGURATION[key]; 
                