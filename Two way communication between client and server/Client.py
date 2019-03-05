import socket

host = 'localhost'
port = 1234
buf = 1024

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))

print("Sending 'client1 to server\\n'")
clientsocket.send(bytes('client1', 'utf-8'))
print("REPLY From Server: ") 
print(clientsocket.recv(buf))

print("Sending 'client2'")
clientsocket.send(bytes('client2', 'utf-8'))
print(clientsocket.recv(buf))

print("Sending 'abc'")
clientsocket.send(bytes('abc', 'utf-8'))
print(clientsocket.recv(buf))

print("Sending 'abc'")
clientsocket.send(bytes('abc', 'utf-8'))
print(clientsocket.recv(buf))


print("Sending 'bye'")
clientsocket.send(bytes('bye', 'utf-8'))
print(clientsocket.recv(buf))

clientsocket.close()
