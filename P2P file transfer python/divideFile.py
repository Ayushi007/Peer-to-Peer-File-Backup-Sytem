import os

def divideFile(filename, num_peers):
    with open(filename, 'rb') as f:
        st = os.stat(filename)
        size = st.st_size
        print(size)
        while(size % num_peers != 0):
            num_peers = num_peers -1
        print(num_peers)
        read_size = int(size/num_peers)
        chunk_list = []
        chunk = str(f.read(read_size),'utf-8')
        while chunk:
            chunk_list.append(chunk)
            chunk = str(f.read(read_size),'utf-8')
    return chunk_list

