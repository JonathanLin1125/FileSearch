from pathlib import Path
from pathlib import *
import shutil

#Prints all of the files in that directory plus all files in its subdirectories
def print_directory_sub(path_obj:"Path(path)"):
    """
    First prints all the files in given directory
    Then iterates through directory again, checking for subdirectories
    If subdirectory is found, it will recursively call the method, starting over
    By printing the subdirectories' info, then checking for more sub-subdirectories....etc
    """
    print_directory(path_obj)
    for file_path in sorted(path_obj.iterdir()):
        path_obj = Path(file_path)
        
        if(path_obj.is_dir() == True):
                print_directory_sub(path_obj)
            
#Prints all of the files in that directory but no subdirectories
def print_directory(path_obj:"Path(path)"):
    for file_path in sorted(path_obj.iterdir()):
        print(file_path)

#Stores all files in directory&subdirectory that has same name as the information (file name inputted by user) in list
#If there are more subdirectories within the directory, function will recursively call itself to find all files
def get_matching_files(path_obj:"Path(obj)", information:str, list_paths:list):
    for file_path in sorted(path_obj.iterdir()):
        path_obj2 = Path(file_path)
        if (path_obj2.is_file() and PurePath(file_path).name.lower() == information):
            list_paths.append(file_path)

    #Iterates twice so that files that are in the directory are printed before its subdirectory files
    for file_path in sorted(path_obj.iterdir()):
        path_obj2 = Path(file_path)
        if (path_obj2.is_dir()):
            get_matching_files(path_obj2, information, list_paths)

#Stores all files in directory&subdirectory that has same extension as the information (extension inputted by user) in list
#If there are more subdirectories within the directory, function will recursively call itself to find all files
def get_matching_extensions(path_obj:"Path(obj)", information:str, list_paths:list):
    for file_path in sorted(path_obj.iterdir()):
        path_obj2 = Path(file_path)
        if (path_obj2.is_file() and PurePath(file_path).suffix.lower() == information):
            list_paths.append(file_path)

    #Iterates twice so that files that are in the directory are printed before its subdirectory files           
    for file_path in sorted(path_obj.iterdir()):
        path_obj2 = Path(file_path)
        if (path_obj2.is_dir()):
            get_matching_extensions(path_obj2, information, list_paths)

#Stores all files in directory&subdirectories and checks if the information (text inputted by user) is in the text file in list
#Function will recursively call itself to find all text files that contain the information
def get_matching_text(path_obj:"Path(obj)", information:str, list_paths:list):
    for file_path in sorted(path_obj.iterdir()):
        try:
            with Path(file_path).open() as file:
                text = file.read()
                if information in text.lower(): #Change if case sensitive
                    list_paths.append(file_path)
        except:
            pass

    #Iterates twice so that files that are in the directory are printed before its subdirectory files           
    for file_path in sorted(path_obj.iterdir()):
        path_obj2 = Path(file_path)
        if (path_obj2.is_dir()):
             get_matching_text(path_obj2, information, list_paths)

#Stores all files in directory&subdirectories whose size is less than or greater than the information (size given by user) in list
#If there are more subdirectories within the directory, function will recursively call itself to find all files
def get_files_smaller_or_greater_than(path_obj:"Path(obj)", information:int, list_paths:list, symbol:str):
    for file_path in sorted(path_obj.iterdir()):
        path_obj2 = Path(file_path)
        if symbol == "<":
            if (path_obj2.is_file() and path_obj2.stat().st_size < information):
                list_paths.append(file_path)
        elif symbol == ">":
            if (path_obj2.is_file() and path_obj2.stat().st_size > information):
                list_paths.append(file_path)

    #Iterates twice so that files that are in the directory are printed before its subdirectory files           
    for file_path in sorted(path_obj.iterdir()):
        path_obj2 = Path(file_path)
        if (path_obj2.is_dir()):
            get_matching_extensions(path_obj2, information, list_paths)

#Prints all the paths that have already been stored in the correct order in paramter list
def print_paths(list_paths:list):
    for path in list_paths:
        print(path)

#Prints first line of each file, if it is not a text, function will print "NOT TEXT"
def print_first_line(list_paths:list):
    for path in list_paths:
        try:
            with Path(path).open() as file:
                text = file.readline().strip()
                print(text)
        except:
            print("NOT TEXT")

#Duplicates each file and stores it in the same directory as the original with the copy having .dup at the end
def dup_files(list_paths:list):
    for path in list_paths:
        shutil.copyfile(str(path), str(path) + ".dup")
    

#Touches each file in list_paths to update time stamp to current time
def touch_files(list_paths:list):
    for path in list_paths:
        Path(path).touch()
    
#Takes action on the files that we have narrowed down
def take_action(list_paths:list):
    letter = input()

    #Makes sure that something is inputted 
    while len(letter) != 1:
        print("ERROR")
        letter = input()

    if(letter == "F"):
        print_first_line(list_paths)
    elif(letter == "D"):
        dup_files(list_paths)
    elif(letter == "T"):
        touch_files(list_paths)
    

#Method reads in input either N, E, T, or < & > with following information
#If letter is invalid or if the following information is invalid, function will print "ERROR"
#Function calls take_action at the end if there are any files in the list of files
def search_characteristics(path_obj:"Path(path)"):
    line = input()

    #Makes sure that line contains information, otherwise next part has index out of range error
    while len(line) < 3:
        print("ERROR")
        line = input()
        
    symbol = line[0]
    information = line[2:len(line)]

    #All matched files will be stored in list_paths
    list_paths = []

    if(symbol != "N" and symbol != "E" and symbol != "T" and symbol != "<" and symbol != ">"):
        print("ERROR")
        search_characteristics(path_obj)
    elif(symbol == "N"):
        get_matching_files(path_obj, information.lower(), list_paths)
    elif(symbol == "E"):       
        #Makes sure that extension works for both Ex: .py and py, takes in account of the lost of the "."
        if information[0] != ".":
            information = "." + information
        get_matching_extensions(path_obj, information.lower(), list_paths)
    elif(symbol == "T"):
        get_matching_text(path_obj, information.lower(), list_paths) #Change if case sensitive
    elif(symbol == "<" or symbol == ">"):
        try:
            try_int = int(information)
            get_files_smaller_or_greater_than(path_obj, try_int, list_paths, symbol)
        except:
            print("ERROR")
            search_characteristics(path_obj)
            
    print_paths(list_paths)

    #Finally goes to the take action on files if there were any files
    if(len(list_paths) > 0):
        take_action(list_paths)
 

#Method reads in either the letter "D" or "R" followed by a valid path to a directory
#If letter is invalid or if path is invalid, function will print "ERROR"
def read_input():
    line = input()

    #Makes sure that line contains information, otherwise next part has index out of range error
    while len(line) < 3:
        print("ERROR")
        line = input()
        
    letter = line[0]
    path = line[2:len(line)]

    path_obj = Path(path)
    if((letter != "D" and letter != "R") or path_obj.exists() == False):
        print("ERROR")
        read_input()
    else:
        if letter == "D":
            print_directory(path_obj)
        elif letter == "R":
            print_directory_sub(path_obj)
        search_characteristics(path_obj)
    
    
if __name__ == "__main__":
    read_input()
