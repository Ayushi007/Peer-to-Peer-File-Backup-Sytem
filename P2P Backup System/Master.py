import socket
import sys
from threading import Thread
from socketserver import ThreadingMixIn
import ast
import fileinput
import glob
#file_list = ['chunk1.txt','chunk2.txt','chunk3.txt']
file_list = glob.glob('./chunk1.txt')


def download(TCP_IP, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, PORT))
    f = open('received_chunks', 'wb')
    print ("receiving data...")
    data=s.recv(BUFFER_SIZE)
    #print('data=%s', (data))
    word = data.split("_")
    print (word[0])
    cha=open(word[0], 'w+') #creates a file for each chunk recived and writes the chunk in it
    cha.write(word[1])
    outfile =open('result.txt', 'w')
    for word[0] in file_list:
        with open(word[0], 'rb') as infile:
            outfile.write(infile.read())
    #if not data:
    #break
    outfile.close()
    s.close()

argv = sys.argv
# Get the server hostname and port as command line arguments
host = argv[1]
TCP_PORT = argv[2]
TCP_IP = "168.150.63.88"
TCP_PORT = int(TCP_PORT)
o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
o.connect_ex((TCP_IP, TCP_PORT))
info = o.recv(1024)
print(TCP_IP, " ", TCP_PORT,"\n")
        
print(o,"\n")
print(info,"\n")
print(file_list,"\n")
ast.literal_eval(info)
#json.loads()
print ("list of peers and files: %s" % str(info))
portlist =dict(zip(info[::2], map(str, info[1::2])))
#print portlist.values()[1]
#name = dict((v,k) for k,v in portlist.items()).get(8889)
#print name

BUFFER_SIZE = 1024
with open('received_chunks', 'wb') as fila:
    print ('file opened')
    while True:
            th = Thread(target=download,args=(TCP_IP,8590))
    #th.daemon= True
            th.start()
            #th = Thread(target=download,args=(TCP_IP,8888))
    #th.daemon= True
            #th.start()
            #th = Thread(target=download,args=(TCP_IP,8889))
    #th.daemon= True
            #th.start()
            if not data:
                break
    fila.close()

print('connection closed')
