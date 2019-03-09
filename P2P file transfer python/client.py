import socket
import sys
import time
import os
from os import path

from threading import Thread
from socketserver import ThreadingMixIn
from divideFile import divideFile
num_peer=0
peer_list=[('127.0.0.1',4322)]
myIp='127.0.0.1'
myPort=4321

def tracker_connect(TCP_IP,PORT):
	s_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_tracker.connect((TCP_IP, PORT))
	while(True):
		peer_list= s_tracker.recv(1024)
		num_peer=len(peer_list)
		time.sleep(20)

def listenPeers():
	tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpsock.bind((myIp, myPort))
	if not os.path.exists('Backup_Store'):
		os.mkdir('Backup_Store')
	while(True):
		tcpsock.listen(5)
		(conn, (ip,port)) = tcpsock.accept()
		print(conn)
		data1=conn.recv(30)
		data1=str(data1,'utf-8')
		if(data1=='Backup'):

			if not os.path.exists('Backup_Store/'+ip):
				os.mkdir('Backup_Store/'+ip)
			data=conn.recv(1024)
			data=str(data,'utf-8')
			print(data)
			#print("look at me!!!")
			fileName=data.split("#",1)[0]
			chunkData=data.split("#",1)[1]
			f = open('Backup_Store/'+ip+'/'+fileName, "w")
			f.write(chunkData)

		elif(data1=='Retrieve'):
			fileName=conn.recv(1024)
			f=open('Backup_Store/'+ip+'/'+fileName, "r")
			data=f.read()
			conn.send(data)


def connect_peer(ip,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print(ip,port)
	s.connect((ip, port))
	print(s)
	return s,ip, port
		              

def backup(socks,chunks, fileName):
	count=0
	for chunk in chunks:
		for sock in socks:
			chunk_id=count
			count+=1
			chunk=fileName+"#"+chunk
			mydata.append(tuple((fileName,chunk_id,sock[1],sock[2])))
			newThread=sendFile(fileName, chunk, sock)
			newThread.start()
			threads.append(newThread)
			
class sendFile(Thread):
    
    def __init__(self,fileName, chunk,sock):
        Thread.__init__(self)
        self.ip = sock[1]
        self.port = sock[2]
        self.sock = sock[0]
        self.fileName=fileName
        self.chunk=chunk
        print (" New thread started for Peer ("+ip+":"+str(port)+")")
    
    def run(self):
    	backup=bytes('Backup','utf-8')
    	self.sock.send(backup)
    	data=bytes(self.chunk,'utf-8')
    	print(data)
    	self.sock.send(data)
    	print(self.sock)
    	#self.sock.close()

def retrieveFile(fileName):
	fileMetadata=[]
	for data in mydata:
		if (data[0]==fileName):
			fileMetadata.append(data[0],data[2], data[3], data[1]) # fileName,ip, port, chunk_id

class getChunk(Thread):
    
    def __init__(self, ip, port, chunkId,fileName):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.chunkId=chunkId
        self.fileName=fileName
        print (" New thread started for Peer ("+ip+":"+str(port)+")")

    
    def run(self):
    	s_getChunk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	s_getChunk.connect((self.ip, self.port))
    	s_getChunk.send('Retrieve')
    	s_getChunk.send(self.fileName)
    	data_retrieved.append(s_getChunk.recv(1024))

def getFile(fileMetadata):
	for data in fileMetadata:
		ip=fileMetadata[1]
		port=fileMetadata[2]
		chunkId=fileMetadata[3]
		fileName=fileMetadata[0]
		newThread=getChunk(ip, port, chunkId,fileName)
		newThread.start()
		rThreads.append(newThread)


threads=[]
rThreads=[]
data_retrieved=[]
#tracker ip and port
TCP_IP='127.0.0.1'
TCP_PORT=3454
#th = Thread(target=tracker_connect,args=(TCP_IP,TCP_PORT))
#th.start()
mydata=[]
th_listen=Thread(target=listenPeers)
th_listen.start()
while(True):
	print('Menu:\n')
	print('1. Backup\n')
	print('2. Retrieve\n')
	choice=input("List your choice")
	if(choice=='1'):
		#print("hihihihiih")
		num_peer_instant=len(peer_list)
		sockets_list=[]
		file_name=input("Enter the filename:")
		for i in range(0, num_peer_instant):
			ip=peer_list[i][0]		#getting ip and port of peer
			port=int(peer_list[i][1])
			sockets_list.append(connect_peer(ip,port)) 
		connections=len(sockets_list)
		chunk_list=divideFile(file_name,connections)
		backup(sockets_list,chunk_list,file_name)

	elif(choice=='2'):
		fileName=input("Enter the file name:")
		flag=0
		for data in mydata:
			if(fileName==data[0]):
				flag=1
		if(flag==0):
			print("Error!!! File not backuped up")
			continue
		fileMetadata=retrieveFile(fileName)
		fileRetrieved=getFile(fileMetadata)
		chunkIds=[]
		for data in fileMetadata:
			chunkIds.append(fileMetadata[3])
		zipped_pairs = zip(chunkIds, data_retrieved) 
		z = [x for _, x in sorted(zipped_pairs)]
		print(z)
		
			
