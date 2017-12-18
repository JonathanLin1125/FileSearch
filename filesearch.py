from pathlib import Path
from pathlib import *
import shutil

#Adds all the files in a given directory to list_paths and then recursively calls itself to continue onto subdirectories
def get_directory_sub(path_obj:"Path(path)", list_paths:list):
    get_directory(path_obj, list_paths)
    for file_path in sorted(path_obj.iterdir()):
        path_obj = Path(file_path)

        if(path_obj.is_dir() == True):
            get_directory_sub(path_obj, list_paths)

#Adds all the files in a given directory to list_paths
def get_directory(path_obj:"Path(path)", list_paths:list):
    for file_path in sorted(path_obj.iterdir()):
        if(Path(file_path).is_dir() == False):
            list_paths.append(file_path)

#Prints all the paths in a given list   
def print_paths(list_paths:list):
    for path in list_paths:
        print(path)

#Iterates through the list of paths that are under consideration and adds the ones that have matching names
def get_matching_files(information:str, list_paths:list, list_matches:list):
    for path in list_paths:
        path_obj = Path(path)
        if(path_obj.is_file() and PurePath(path).name.lower() == information):
            list_matches.append(path)

#Iterates through the list of paths that are under consideration and adds the ones that have matching extensions
def get_matching_extensions(information:str, list_paths:list, list_matches:list):
    for path in list_paths:
        path_obj = Path(path)
        if(path_obj.is_file() and PurePath(path).suffix.lower() == information):
            list_matches.append(path)

#Tries to open each path as a text file, if it is able to open, function will check to see
#If the user's input exists in the text file
def get_matching_text(information:str, list_paths:list, list_matches:list):
    for path in list_paths:
        try:
            file = open(path, "r")
            text = file.read()
            if information in text.lower(): #CHANGE IF CASE SENSITIVE
                list_matches.append(path)
            file.close()
        except:
            pass

#Iteratres through the list of paths that are under consideration and adds the ones that are either less than or greater than the
#file size specified by user to the list, list_matches
def get_files_smaller_or_greater_than(information:int, list_paths:list, list_matches:list, symbol:str):
    for path in list_paths:
        path_obj = Path(path)
        if symbol == "<":
            if(path_obj.is_file() and path_obj.stat().st_size < information):
                list_matches.append(path)
        elif symbol == ">":
            if(path_obj.is_file() and path_obj.stat().st_size > information):
                list_matches.append(path)

#Opens each file, or tries to, and prints the first line
#If file is not text, function prints "NOT TEXT"
def print_first_line(list_matches:list):
    for path in list_matches:
        try:
            with Path(path).open() as file:
                text = file.readline().strip()
                print(text)
        except:
            print("NOT TEXT")
            
#Duplicates all files in the list and adds extension .dup
def dup_files(list_matches:list):
    for path in list_matches:
        shutil.copyfile(str(path), str(path) + ".dup")

#Touches each file and updates the timestamp to the current time
def touch_files(list_matches:list):
    for path in list_matches:
        Path(path).touch()

"""
Last part of the program asks for a single letter of input
If letter is not F, D, or T, functin prints "ERROR" and restarts
Function calls corresponding functions based of user input and passes in the list_matches, list of paths that are to be edited
"""
def take_action(list_matches:list):
    letter = input()

    #Makes sure that something is inputted 
    while ((len(letter) != 1) or (letter != "F" and letter != "D" and letter != "T")):
        print("ERROR")
        letter = input()

    if(letter == "F"):
        print_first_line(list_matches)
    elif(letter == "D"):
        dup_files(list_matches)
    elif(letter == "T"):
        touch_files(list_matches)

"""
Reads the first letter/symbol of user input and calls function based on letter chosen.
If the first letter not a valid letter/symbol, the function will print "ERROR" and reprompt.
If input is "E" followed by an extension, function will check that the followed input has a "." before the extension, if not
function will add it automatically.
If symbol is "<" and ">", function will test if the followed number is a valid integer, if not, function will print "ERROR" and
restart for user to retry input.
Function will store all paths that are in search in list_matches and prints it at the end of the function.
If the list_matches has any info, then the function will call the last part of the program. If list is empty, program ends.
"""
def search_characteristics(list_paths:list):
    looper = True

    #Keeps looping until input is valid
    while(looper):
        line = input()

        symbol = None
        information = None
        
        #Lots of defense for if user input is not valid
        if(len(line) > 2):
            if(line[1] == " "):
                symbol = line[0]
                information = line[2:len(line)]
        elif(len(line) == 1):
            symbol = line[0]

        list_matches = []

        #Makes sure that symbol is valid
        if(symbol != "N" and symbol != "E" and symbol != "T" and symbol != "A" and symbol != "<" and symbol != ">"):
            print("ERROR")
        #Checks that only input "A" allows for single letter input
        elif((symbol == "N" or symbol == "E" or symbol == "T" or symbol == "<" or symbol == ">") and information == None):
            print("ERROR")
        else:
            looper = False


    if(symbol == "N"):
        get_matching_files(information.lower(), list_paths, list_matches)
    elif(symbol == "E"):       
        #Makes sure that extension works for both Ex: .py and py, takes in account of the lost of the "."
        if information[0] != ".":
            information = "." + information
        get_matching_extensions(information.lower(), list_paths, list_matches)
    elif(symbol == "T"):
        get_matching_text(information.lower(), list_paths, list_matches) #Change if case sensitive
    elif(symbol == "A"):
        if(symbol + information != "A"):
            print("ERROR")
            search_characteristics(list_paths)
        else:
            list_matches = list_paths
    elif(symbol == "<" or symbol == ">"):
        try:
            #Makes sure that information entered is a valid integer
            try_int = int(information)
            get_files_smaller_or_greater_than(try_int, list_paths, list_matches, symbol)
        except ValueError:
            print("ERROR")
            #If information is not an int, function restarts
            search_characteristics(list_paths)
            
    print_paths(list_matches)

    #Finally goes to the take action on files if there were any files
    if(len(list_matches) > 0):
        take_action(list_matches)

"""
Reads the first input of the user, either D or R followed by a VALID path.
If either input is invalid, function will print "ERROR" and allow the user to retry.
Once input is deemed valid, function will get all paths in directory/subdirectory according
to user input and store information in the list, list_paths.
Finally, program will call print_paths(list_paths) to get the list printed in the console and move on
to the next section of the program, search_characerteristics, to narrow the search for specific files.
"""
def read_input():
    looper = True

    #Keep looping until input is valid
    while(looper):
        line = input()

        #Makes sure that line contains information, otherwise next part has index out of range error
        while len(line) < 3:
            print("ERROR")
            line = input()

        #Splits input into two parts, first letter, and the rest of the line after the first space
        letter = line[0]
        path = line[2:len(line)]

        #List_paths will store all strings of paths, this list is used throughout since functions pass
        #lists as references and not variables
        list_paths = []

        #Checks if letter is a valid choice and if the path exists
        path_obj = Path(path)
        if((letter != "D" and letter != "R") or path_obj.exists() == False or line[1] != " "):
            print("ERROR")
        else:
            looper = False
    #Calls function based of if recursion is needed
    if letter == "D":
        get_directory(path_obj, list_paths)
    elif letter == "R":
        get_directory_sub(path_obj, list_paths)
            
    #Print paths stored in list_paths
    print_paths(list_paths)

    search_characteristics(list_paths)
    
if __name__ == "__main__":
    read_input()
