"""
Name: Jonathan Lin
ID: 13588198
"""

#Check to see if input is integer
def try_int()->int:
    while True:
        try:
            num = int(input())
            return num
        except ValueError:
            print("",end="")
            
#Prints the blocks with number based off input
def main():
    num = try_int()
    if num > 0:
        print("+-+")
        print("| |")
        for i in range(num-1):
            print(" " * (i * 2), end="")
            print("+-+-+")
            print(" " * (i *2), end="")
            print("  | |")
        print(" " * ((num-1)*2), end="")
        print("+-+")

main()

        
