import requests
import json
import subprocess
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

config = dotenv_values(); 
username = config.get('USERNAME'); 
branch = config.get('BRANCH_TO_PUSH'); 
local_repo_path = config.get('LOCAL_REPO_PATH'); 
file_name = config.get('KATA_FILE_NAME'); 
push_step = config.get('PUSH_STEP'); 

def run(): 
    req = requests.get('https://www.codewars.com/api/v1/users/Mecopi'); 
    resJSON = json.loads(req.content); 
    print(json.dumps(resJSON, indent=4)); 

# run(); 


# Output

# bashCommand = "echo Hello World!"; 
# process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE); 
# output, error = process.communicate(); 