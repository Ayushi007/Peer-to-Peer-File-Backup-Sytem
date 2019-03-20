import os

import math



def divideFile(filename, num_peers):

    with open("main/"+filename, 'r') as f:

        st = os.stat("main/"+filename)

        size = st.st_size

        #print(size)

        #print(num_peers)



        read_size = int(math.ceil(size/num_peers))

        #print("Chunk size rounded is --****************", read_size)

        chunk_list = []

        chunk = f.read(read_size)

        while chunk:

            chunk_list.append(chunk)

            chunk = f.read(read_size)

        return chunk_list

