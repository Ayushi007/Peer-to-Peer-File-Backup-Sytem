import socket
import sys
import time
import os
from os import path
import collections
import pickle

from threading import Thread
from socketserver import ThreadingMixIn
from divideFile import divideFile

num_peer=0
peer_list=[]
myIp='0.0.0.0'
track_ip = '192.168.43.131'
myPort=4322
tracker_port = 4321
def notify_tracker():
	s_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_tracker.connect((track_ip, 4320))
	msg = 'Hello'
	data = pickle.dumps(msg)
	s_tracker.send(data)
	s_tracker.close()
	print("Im in!")


def tracker_connect():
	s_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_tracker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s_tracker.bind((myIp, tracker_port))
	print("Listening to tracker...")
	while(True):
		s_tracker.listen(5)
		(conn, (ip,port)) = s_tracker.accept()
		data = conn.recv(1024)
		#################################
		new_list=pickle.loads(data)
		new_list=set(new_list)-set(peer_list)
		peer_list.extend(list(new_list))
		#################################
		print(peer_list)
		num_peer=len(peer_list)


def listenPeers():
	tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpsock.bind((myIp, myPort))
	print("Listening to peers...")

	if not os.path.exists('Backup_Store'):
		os.mkdir('Backup_Store')
	while(True):
		tcpsock.listen(5)
		(conn, (ip,port)) = tcpsock.accept()
		data1=conn.recv(8)
		data1=str(data1, 'utf-8')
		if '#' in data1:
			data2=data1.split("#", 1)[0]
			numrep=int(data1.split("#",1)[1])
			if (data2=='Backup'):
				while(numrep):
					if not os.path.exists('Backup_Store/'+ip):
						os.mkdir('Backup_Store/'+ip)
					data=conn.recv(1024)
					data=str(data, 'utf-8')
					fileName=data.split("#", 2)[0]
					fileWoutExt=fileName.split(".", 1)[0]
					Ext=fileName.split(".", 1)[1]
					chunkId=data.split("#", 2)[1]
					chunkData=data.split("#", 2)[2]
					FinalFileName=fileWoutExt+"_"+chunkId+"."+Ext
					dataprint = [chunkData]
					print("\nReceived backup chunk ", str(dataprint), " of file ",fileName," from IP ", ip)
					print("Chunk stored in Backup_Store/"+ip+"/"+FinalFileName,"\n")
					writeData=chunkData.split("/n")

					with open('Backup_Store/'+ip+'/'+FinalFileName, "w") as f1:
						for item in writeData:
							f1.write("%s" %item)
					f1.close()
					numrep-=1

		elif(data1=='Retrieve'):
			fileName=conn.recv(1024)
			f=open("Backup_Store/"+ip+'/'+str(fileName, 'utf-8'), "r")
			data=f.read()
			dataprint = [data]
			print("Sending backed up chunk data ", str(dataprint), " to IP ", ip)
			conn.send(bytes(data, 'utf-8'))
		conn.close()
		print('\nMenu:\n')
		print('1. Backup\n')
		print('2. Retrieve\n')
		print("List your choice: ")


def connect_peer(ip,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((ip, port))
	except Exception as e:
		print("Exception is ", e)
		return False
	return s,ip, port


def backup(socks,chunks, fileName,repeat):
 	#chunks=chunk_list     socket_list= socket, ip, port
	count=0
	n = 0
	flag = {}
	cnt_rep = 0
	for sock in socks:
		flag[sock] = 0
	while n<repeat:
		for sock in socks:
			cnt_rep+=1
			if flag[sock] == 0 :
				backup=bytes('Backup#'+str(repeat),'utf-8')
				sock[0].send(backup)
				flag[sock] = 1
			#time.sleep(1)
			chunk_id=count
			chunk = chunks[count]
			chunkprint = [chunk]
			print("Chunk " +str(chunkprint)+ " being sent to IP "+sock[1])
			chunk=fileName+"#"+str(chunk_id)+"#"+chunk
			mydata.append(tuple((fileName,chunk_id,sock[1],sock[2])))
			newThread=sendFile(fileName, chunk, sock)
			newThread.start()
			threads.append(newThread)
			if(cnt_rep==repeat):
				count+=1
				cnt_rep = 0
		n+=1


class sendFile(Thread):
    def __init__(self,fileName, chunk,socks):
        Thread.__init__(self)
        self.ip = socks[1]
        self.port = socks[2]
        self.sock = socks[0]
        self.fileName=fileName
        self.chunk=chunk


    def run(self):
    	#backup=bytes('Backup','utf-8')
    	#self.sock.send(backup)
    	data=bytes(self.chunk,'utf-8')
    	self.sock.send(data)


def retrieveFile(fileName):
    fileMetadata=[]
    for data in mydata:
        if (data[0]==fileName):
            fileMetadata.append(tuple((data[0],data[2], data[3], data[1]))) # fileName,ip, port, chunk_id
    return fileMetadata


class getChunk(Thread):
	def __init__(self, ip, port, chunkId,fileName):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.chunkId=chunkId
		self.fileName=fileName
		self.ext=fileName.split('.', 1)[1]
		self.chunk_file=fileName.split('.', 1)[0]+"_"+str(chunkId)+"."+self.ext


	def run(self):
		s_getChunk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_getChunk.settimeout(2)
		try:
			s_getChunk.connect((self.ip, self.port))
		except Exception as e:
			connectionFails.append(self.ip)
			print("Exception ", e)
			print(e)
			return
		s_getChunk.settimeout(None)
		s_getChunk.send(bytes('Retrieve', 'utf-8'))
		#time.sleep(1)
		s_getChunk.send(bytes(self.chunk_file, 'utf-8'))
		data_i_got = s_getChunk.recv(1024)
		data_i_got = str(data_i_got, 'utf-8')
		chunkprint = [data_i_got]
		print("Chunk " + str(chunkprint)+ " retrieved from IP - "+self.ip)
		data_retrieved.update({self.chunkId : data_i_got})


def getFile(fileMetadata):
	for data in fileMetadata:
		ip=data[1]
		port=data[2]
		chunkId=data[3]
		fileName=data[0]
		if chunkId not in data_retrieved.keys():
			if ip not in connectionFails:
				newThread=getChunk(ip, port, chunkId, fileName)
				newThread.start()
				newThread.join()
				rThreads.append(newThread)


threads=[]
rThreads=[]
lthreads=[]
data_retrieved={}
connectionFails=[]

notify_tracker()
#tracker ip and port

mydata=[]
th_track=Thread(target=tracker_connect)
th_track.start()

th_listen=Thread(target=listenPeers)
th_listen.start()


while(True):
	print('\nMenu:\n')
	print('1. Backup\n')
	print('2. Retrieve\n')
	choice=input("List your choice: ")
	if(choice=='1'):
		num_peer_instant=len(peer_list)
		sockets_list=[]
		file_name=input("Enter the filename: ")
		if not(os.path.isfile(file_name)):
			print("File does not exist.")
			continue
		print('\nSub-Menu:\n')
		print('1, High Priority File (3 copies will be created)\n')
		print('2. Low Priority File (2 copies will be created)\n')

		choice1=input("List your choice: ")
		if(choice1=='1'):
			n=3
			print("Backing up 3 copies")
		else:
			n=2
			print("Backing up 2 copies")

		print(peer_list)
		for i in range(0, len(peer_list)):
			ip=peer_list[i][0]		#getting ip and port of peer
			port=int(peer_list[i][1])
			conn=connect_peer(ip, port)
			if(conn!=False):
				sockets_list.append(conn)
		connections=len(sockets_list)

		if connections ==0:
			print("No peers connected - Try later!!")
			continue

		chunk_list=divideFile(file_name,connections)
		print("Chunks created :", chunk_list)
		print("# of Conections: ", connections)
		backup(sockets_list,chunk_list,file_name,n)

	elif(choice=='2'):
        #data_retrieved = {}
		fileName=input("Enter the file name: ")
		flag=0
		for data in mydata:
			if(fileName==data[0]):
				flag=1
		if(flag==0):
			print("Error!!! File not backed up")
			continue
		fileMetadata=retrieveFile(fileName)
		getFile(fileMetadata)
		z=[]
		od=collections.OrderedDict(sorted(data_retrieved.items()))
		for k, v in od.items():
			z.append(v)
		f=open("new"+fileName, "w")
		for data1 in z:
			f.write("%s" %data1)
		f.close()
		print("Final File retrieved - ", z)
