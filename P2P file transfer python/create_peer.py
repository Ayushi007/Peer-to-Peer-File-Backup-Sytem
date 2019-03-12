import subprocess
import csv
import os
import socket
import pickle

name = input("Enter a name for the instance: ")
filename = name+".txt"
ip = ""
client = "tracker_run_peer.py divideFile.py"
HOST = '10.138.0.27'
PORT = 4320

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

connected = 0
while connected == 0:
    subprocess.call(["./push_client.sh", name, client])
    connected = int(input("connected? "))
    print(connected)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = pickle.dumps(ip)
s.send(data)
s.close()
print("Notified the tracker")
subprocess.call(["./run_client.sh", name, client])
