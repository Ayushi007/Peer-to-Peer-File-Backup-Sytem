import socket
from threading import Thread
from socketserver import ThreadingMixIn
import json

TCP_IP = '168.150.63.88'
TCP_PORT = 9001
BUFFER_SIZE = 1024
file_list = {"chunk1.txt":8590}

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print (" New thread started for "+ip+":"+ str(port))

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    print ("*******************************************************************************************")
    print ("                           Peer 1            Peer 2                Peer 3                           ")
    print ("Current Peers connected: %s" % str (file_list))
    print ("*******************************************************************************************")
    (conn, (ip,port)) = tcpsock.accept()
    data = json.dumps(file_list)
    conn.send(data)
    conn.close()
    
    print ('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
