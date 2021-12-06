import hashlib
from mpi4py import MPI
import json
import time


class score():

    def __init__(self, fnames):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.names = [hashlib.md5, hashlib.sha1, hashlib.sha224,
                      hashlib.sha256, hashlib.sha384, hashlib.sha512]
        self.fnames = fnames
#{'blake2b', 'sha1', 'sha3_256', 'sha224', 'shake_256', 'sha256', 'sha512', 'sha3_384', 'sha3_512', 'blake2s', 'sha3_224', 'shake_128', 'md5', 'sha384'}

    def hash_bytestr_iter(self, bytesiter, hasher):
        for block in bytesiter:
            hasher.update(block)
        return hasher.hexdigest()

    def file_as_blockiter(self, afile, blocksize=65536):
        with afile:
            block = afile.read(blocksize)
            while len(block) > 0:
                yield block
                block = afile.read(blocksize)

    def hashfunctions(self, name, fname):
        return(str(self.hash_bytestr_iter(self.file_as_blockiter(open(fname, 'rb')), name())))

    def writeasjson(self, fname, Dict):
        json_object = json.dumps(Dict, indent=1)

        output_file = 'hash_output/'+fname.split('/')[1] + '.json'

        with open(output_file, "w") as outfile:
            outfile.write(json_object)

    def parallel_hashing(self):

        if (self.rank == 0):
            start = time.time()

        for fname in self.fnames:

            myDict = {}

            for i in range(self.rank, len(self.names), self.size):
                myDict[self.names[i].__name__] = self.hashfunctions(
                    self.names[i], fname)

            completeDict = self.comm.gather(myDict, root=0)

            if(self.rank == 0):
                for Dict in completeDict:
                    for dictEle in Dict:
                        myDict[dictEle] = Dict[dictEle]
                myDict['Available Algorithms:'] = str(
                    hashlib.algorithms_guaranteed)

                self.writeasjson(fname, myDict)
        if(self.rank == 0):
            end = time.time()
            total_time = {}
            total_time['Paralle_CHF_time'] = end-start
            self.writeasjson('input_files/time', total_time)

    def paralle_file_hasher(self):
        if (self.rank == 0):
            start = time.time()
        for i in range(self.rank, len(self.fnames), self.size):

            myDict = {}

            for j in range(len(self.names)):
                myDict[self.names[j].__name__] = self.hashfunctions(
                    self.names[j], self.fnames[i])
            self.writeasjson(self.fnames[i], myDict)
        if(self.rank == 0):
            end = time.time()
            total_time = {}
            total_time['Paralle_File_Hashing_Time'] = end-start
            self.writeasjson('input_files/time', total_time)

    def check_intigrity(self):
        for i in range(self.rank, len(self.names), self.size):
            print(str(self.names[i].__name__) + ":\t", end="")
            if(self.hashfunctions(self.names[i], self.fnames[0]) == self.hashfunctions(self.names[i], self.fnames[1])):
                print("PASS")
            else:
                print("FAIL")

    def serial_hashing(self):

        start = time.time()

        for i in range(0, len(self.fnames)):

            myDict = {}

            for j in range(len(self.names)):
                myDict[self.names[j].__name__] = self.hashfunctions(
                    self.names[j], self.fnames[i])
            self.writeasjson(self.fnames[i], myDict)

        end = time.time()
        total_time = {}
        total_time['Serial_Hashing_Time'] = end-start
        self.writeasjson('input_files/time', total_time)
