import requests
import json
from dotenv import load_dotenv

load_dotenv(); 
req = requests.get('https://www.codewars.com/api/v1/users/Mecopi'); 
resJSON = json.loads(req.content); 

print(json.dumps(resJSON, indent=4)); 

