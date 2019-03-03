import os

def divideFile(filename, num_peers):
    with open(filename, 'rb') as f:
        st = os.stat(filename)
        size = st.st_size
        print(size)
        while(size % num_peers != 0):
            num_peers = num_peers -1
        print(num_peers)
        read_size = size/num_peers
        chunk_list = []
        chunk = f.read(read_size)
        while chunk:
            chunk_list.append(chunk)
            chunk = f.read(read_size)
    return chunk_list

def copyFile(original_name, new_name):
    chunk_list = divideFile(original_name, 4)
    with open(new_name, 'wb') as f:
        for chunk in chunk_list:
            f.write(chunk)

copyFile('chapter 30.pdf','copied_chapter_30.pdf')
