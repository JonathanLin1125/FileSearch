'''
Created on Aug 23, 2017

@author: jonathanlin
'''
import pathlib

def read_input()->str:
    path = input()
    while not pathlib.Path(path).exists():
        path = input()
    return path

def check_size(path_obj:str):
    total_size = 0.0
    
    for item in path_obj.iterdir():
        item_obj = pathlib.Path(item)
        if item_obj.is_file() == False:
            total_size += check_size(item_obj)
        else:
            total_size += item_obj.stat().st_size
            
    return total_size
            

if __name__ == "__main__":
    path = read_input()
    size = check_size(pathlib.Path(path))
    print(str(size * 0.000000001) + " gb")