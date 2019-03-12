import socket
import pickle
from threading import Thread
import time

peer_list = []
HOST = '0.0.0.0'
PORT = 4320
CLIENT_PORT = 4322
TRACK_PORT = 4321

def connect_peer(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    i = 0
    while i < 10:
	    try:
	        s.connect((ip, port))
	    except Exception as e:
		    time.sleep(1)
		    i = i + 1
		    continue
	    break

    if i == 10:
	    return False
    return s, ip

class send_lis(Thread):

    def __init__(self, sock, data):
        Thread.__init__(self)
        self.sock = sock[0]
        self.data = data

    def run(self):
        self.sock.send(self.data)


def notify_peers():
    sock_list = []
    threads = []
    if len(peer_list) != 1:
        for peer in peer_list:
            sock = connect_peer(peer, TRACK_PORT)
            if sock != False:
            	sock_list.append(sock)
            else:
                print("Cannot connect to ",peer)
        for sock in sock_list:
            new_lis = peer_list.copy()
            new_lis.remove(sock[1])
            tup = (new_lis, CLIENT_PORT)
            data = pickle.dumps(tup)
            newThread = send_lis(sock, data)
            newThread.start()
            threads.append(newThread)
        print("Notification sent")

while(True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    data = conn.recv(1024)
    ip = pickle.loads(data)
    peer_list.append(ip)
    print(peer_list)
    time.sleep(3)
    notify_peers()
    s.shutdown(socket.SHUT_RDWR)
