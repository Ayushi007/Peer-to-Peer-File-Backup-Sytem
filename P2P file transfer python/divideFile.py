import os
import math

def divideFile(filename, num_peers):
        f = open(filename, 'r')
        st = os.stat(filename)
        size = st.st_size
        read_size = int(math.ceil(size/num_peers))
        #print("Ceiled size------",read_size)
        chunk_list = []
        chunk = f.read(read_size)
        while chunk:
            #print("Chunk---",chunk)
            chunk_list.append(chunk)
            chunk = f.read(read_size)
        return chunk_list

