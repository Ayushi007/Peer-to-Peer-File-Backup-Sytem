import socket
import sys

from threading import Thread
from socketserver import ThreadingMixIn

argv = sys.argv
# Get the server hostname and port as command line arguments
host = argv[1]
TCP_PORT = argv[2]
TCP_PORT = int(TCP_PORT)

TCP_IP = "127.0.0.1"
BUFFER_SIZE = 1024

class ClientThread(Thread):
    
    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print (" New thread started for Peer "+ip+":"+str(port)+")")
    
    def run(self):
        filename='chunk1.txt'
        f = open(filename,'rb')
        while True:
            l = f.readlines(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break
            str1=filename+"_";
            #print(l1[0])
            len1=len(l)
            for i in range(0,len1):
                l1=str(l[i],'utf-8')
                print(l1)
                str1 = str1+l1

            str1=bytes(str1, 'utf-8')

            print(str1)
            self.sock.send(str1)
            print('Chunk Sent ',repr(str1))
                
            

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []
print ("Hello!!")

while True:
    tcpsock.listen(1)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    
    print(conn)
    print ("Got connection from ", (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
