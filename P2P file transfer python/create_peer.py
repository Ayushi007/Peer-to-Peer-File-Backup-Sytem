import subprocess
import csv
import os
import socket

name = raw_input("Enter a name for the instance: ")
filename = name+".txt"
ip = ""
client = "hello_world.py"
HOST = '127.0.0.1'
PORT = 8080

if os.path.isfile("./"+filename) == 0:
    subprocess.call(["./create_instance.sh",name])

with open(filename) as f:
        data = f.readlines()
        reader = csv.reader(data)
        next(reader)
        row = next(reader)
        #list = row[0].strip()
        #ip = list[3]
        ip = (row[0].split())[3]

subprocess.call(["./push_client.sh", name, client])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(bytes(ip))
s.close()
print("Notified the tracker")
