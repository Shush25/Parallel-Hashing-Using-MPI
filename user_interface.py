import os
import json

fileDict = {}
arr = []

os.system('cls')
print("<<< FILE HASH AND INTIGRITY CHECKER >>>\n\n")
print("1. Calculate File Hash\n2. Check File Intigrity\n0. Exit\n\nEnter Choice: ")

choice = int(input())

if(choice == 1):
    os.system('cls')
    print("<<< FILE HASH AND INTIGRITY CHECKER >>>\n\n")
    print("1. Parallalize CHF Calculator\n2. Parallalize Files\n\nEnter Choice: ", end='')
    fileDict["p_type"] = int(input())

    if(fileDict["p_type"] == 1 or 2):
        os.system('cls')
        print("<<< PARALLEL CHF CALCULATOR >>>\n\n")
        print("Enter Number of Files: ", end='')
        n = int(input())
        for i in range(n):
            print(f'File Name[{i+1}]: ', end='')
            arr.append("input_files/" + input())
        fileDict['arr'] = arr

        json_object = json.dumps(fileDict, indent=1)

        with open("input_file.json", "w") as outfile:
            outfile.write(json_object)
        os.system('mpiexec -n 4 python main_file.py')
    else:
        print("Invalid Input!")

elif(choice == 2):
    os.system('cls')
    print("<<< FILE INTIGRITY CHECKER >>>\n\n")
