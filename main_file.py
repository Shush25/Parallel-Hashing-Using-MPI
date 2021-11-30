from hasher import score
import json

with open('input_file.json', 'r') as openfile:
    json_object = json.load(openfile)

arr = json_object['arr']
p_type = json_object['p_type']
obj = score(arr)
if(p_type == 1):
    obj.parallel_hashing()
elif(p_type == 2):
    obj.paralle_file_hasher()