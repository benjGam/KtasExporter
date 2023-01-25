import gvars 

def add_kata_in_file(repo_path, file_name, toWrite): 
    f = open(repo_path + '/' + file_name, "a"); 
    f.write(toWrite); 
    f.close(); 

def read_kata_file(repo_path, file_name):
    try:
        f = open(repo_path + '/' + file_name, 'r'); 
        content = file.read(); 
        for line in content: 
            if()
    except: 
        return; 