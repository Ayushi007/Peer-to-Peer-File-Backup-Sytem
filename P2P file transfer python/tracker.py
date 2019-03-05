import socket

peer_list = []
HOST = '127.0.0.1'
PORT = 8080

def notify_peers():
    print("Notification sent")

while(True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    ip = conn.recv(1024)
    peer_list.append(ip)
    print(peer_list)
    s.shutdown(socket.SHUT_RDWR)
