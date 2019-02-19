import socket
import sys

from threading import Thread
from socketserver import ThreadingMixIn

argv = sys.argv
# Get the server hostname and port as command line arguments
host = argv[1]
TCP_PORT = argv[2]
TCP_PORT = int(TCP_PORT)

TCP_IP = "168.150.63.88"
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
            l = f.read(BUFFER_SIZE)
            while (l):
                str = filename + "_" + l
                self.sock.send(str)
                print('Chunk Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break

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
