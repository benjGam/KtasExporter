import gvars 
from Kata import Kata
import traceback

def add_kata_in_file(repo_path, file_name, toWrite): 
    f = open(repo_path + '/' + file_name, "a"); 
    f.write(toWrite); 
    f.close(); 

def read_kata_file(repo_path, file_name):
    try:
        f = open(repo_path + '/' + file_name, 'r'); 
        content = f.readlines();  
        for line in content: 
            if(line[0] == '#' and "kyu" in line.lower()):
                kata_title = line[1:line.rfind('#')].strip(); 
                gvars.already_pushed_katas.append(kata_title);  
    except Exception as e:
        print(e); 
        exit; 