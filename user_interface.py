import os
import json
myDict = {}
arr = []
print("Enter the number of files to hash: ")
n = int(input())
for i in range(n):
    print("Enter the file name of file ", i+1)
    arr.append("input_files/"+input())
myDict['arr'] = arr

print("\nEnter which function you want to use: ")
print("1. Parallel hash functions")
print("2. Parallel hash multiple files")
myDict['p_type'] = int(input())

json_object = json.dumps(myDict, indent=1)

with open("input_file.json", "w") as outfile:
    outfile.write(json_object)
os.system('mpiexec -n 4 python main_file.py')
