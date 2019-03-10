import socket
import sys
import time
import os
from os import path
import collections

from threading import Thread
from socketserver import ThreadingMixIn
from divideFile import divideFile
num_peer=0
peer_list=()
myIp='0.0.0.0'
myPort_tracker=4321
myPort=4322

def tracker_connect(TCP_IP,PORT):
	tcpsock_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpsock_tracker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpsock_tracker.bind((myIp, myPort_tracker))
	while True:
		tcpsock_tracker.listen(2)
		(conn,(ip,port))=tcpsock_tracker.accept()
		print(conn)
		data=conn.recv(2048)
		peer_list=pickle.loads(data)



def listenPeers():
	tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpsock.bind((myIp, myPort))
	print("Listening....")
	if not os.path.exists('Backup_Store'):
		os.mkdir('Backup_Store')
	while(True):
		tcpsock.listen(5)
		(conn, (ip,port)) = tcpsock.accept()
		print(conn)
		#newThread = listen_new_connection(conn, ip, port)
		#newThread.start()
		#lthreads.append(newThread)
		data1=conn.recv(1024)
		data1=str(data1, 'utf-8')
		print(data1)
		if '#' in data1:
			data2=data1.split("#", 1)[0]
			numrep=int(data1.split("#",1)[1])

			if (data2=='Backup'):
				while(numrep):
					if not os.path.exists('Backup_Store/'+ip):
						os.mkdir('Backup_Store/'+ip)
					data=conn.recv(1024)
					data=str(data, 'utf-8')
					print(data)
					fileName=data.split("#", 2)[0]
					fileWoutExt=fileName.split(".", 1)[0]
					Ext=fileName.split(".", 1)[1]
					chunkId=data.split("#", 2)[1]
					chunkData=data.split("#", 2)[2]
					FinalFileName=fileWoutExt+"_"+chunkId+"."+Ext
					print(chunkData)

					writeData=chunkData.split("/n")
					print("ddddddd0")
					with open('Backup_Store/'+ip+'/'+FinalFileName, "w") as f1:
						for item in writeData:
							f1.write("%s\n" %item)
					f1.close()
					numrep-=1
				print("END=======")
		elif(data1=='Retrieve'):
			print("Retrieve")
			fileName=conn.recv(1024)
			print(str(fileName, 'utf-8'))
			f=open("Backup_Store/"+ip+'/'+str(fileName, 'utf-8'), "r")
			data=f.read()
			print(data)
			conn.send(bytes(data, 'utf-8'))
		conn.close()



def connect_peer(ip,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print(ip,port)
	s.connect((ip, port))
	return s,ip, port

def backup(socks,chunks, fileName,repeat):
 #chunks=chunk_list socket_list= socket, ip, port
	count=0
	n = 0
	flag = {}
	cnt_rep = 0
	for sock in socks:
		flag[sock] = 0
	while n<repeat:
		for sock in socks:
			print(sock)
			cnt_rep+=1
			if flag[sock] == 0 :
				backup=bytes('Backup#'+str(repeat),'utf-8')
				sock[0].send(backup)
				flag[sock] = 1
			time.sleep(2)
			chunk_id=count
			chunk = chunks[count]
			print("chunk being sent is:"+ chunk)
			print("------------")
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
        print (" New thread started for Peer ("+ip+":"+str(port)+")")

    def run(self):
    	#backup=bytes('Backup','utf-8')
    	#self.sock.send(backup)
    	data=bytes(self.chunk,'utf-8')
    	print(data)
    	self.sock.send(data)
    	time.sleep(2)
    	#print(self.sock)
    	#self.sock.close()



def retrieveFile(fileName):
    fileMetadata=[]
    for data in mydata:
        if (data[0]==fileName):
            print(data)
            fileMetadata.append(tuple((data[0],data[2], data[3], data[1]))) # fileName,ip, port, chunk_id
            print(fileMetadata)
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
		print (" New thread started for Peer ("+ip+":"+str(port)+")")

	def run(self):
		s_getChunk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s_getChunk.connect((self.ip, self.port))
		except Exception as e:
			return
		#finally:
			#s_getChunk.close()
		print(self.chunk_file)
		s_getChunk.send(bytes('Retrieve', 'utf-8'))
		time.sleep(2)
		s_getChunk.send(bytes(self.chunk_file, 'utf-8'))
		data_i_got=s_getChunk.recv(1024)
		data_i_got=str(data_i_got, 'utf-8')
		print(data_i_got)
		data_retrieved.update({self.chunkId : data_i_got})


def getFile(fileMetadata):
	for data in fileMetadata:
		ip=data[1]
		port=data[2]
		chunkId=data[3]
		fileName=data[0]
		if chunkId not in data_retrieved.keys():
			newThread=getChunk(ip, port, chunkId, fileName)
			newThread.start()
			newThread.join()
			rThreads.append(newThread)
		#newThread=getChunk(ip, port, chunkId,fileName)
		#newThread.start()
		#rThreads.append(newThread)


threads=[]
rThreads=[]
lthreads=[]
data_retrieved={}
#tracker ip and port
TCP_IP='127.0.0.1'
TCP_PORT=3454
th = Thread(target=tracker_connect,args=(TCP_IP,TCP_PORT))
th.start()

mydata=[]
th_listen=Thread(target=listenPeers)
th_listen.start()
#listenPeers()

while(True):
	print('Menu:\n')
	print('1. Backup\n')
	print('2. Retrieve\n')
	choice=input("List your choice: ")
	if(choice=='1'):
		#print("hihihihiih")
		num_peer_instant=len(peer_list[0])
		sockets_list=[]
		file_name=input("Enter the filename: ")
		for i in range(0, num_peer_instant):
			ip=peer_list[0][i]		#getting ip and port of peer
			port=int(peer_list[1])
			sockets_list.append(connect_peer(ip,port))
 #socket_list= socket, ip, port
		connections=len(sockets_list)
		chunk_list=divideFile(file_name,connections)
		n = 2 #chunks to be repeated
		print("Chunk List:", chunk_list)
		print("Conections: ", connections)
		backup(sockets_list,chunk_list,file_name,n)
		#os.remove(file_name)
	elif(choice=='2'):
		fileName=input("Enter the file name: ")
		flag=0
		for data in mydata:
			if(fileName==data[0]):
				flag=1
		if(flag==0):
			print("Error!!! File not backuped up")
			continue
		fileMetadata=retrieveFile(fileName)
		getFile(fileMetadata)
		z=[]
		od=collections.OrderedDict(sorted(data_retrieved.items()))
		print(od)
		for k, v in od.items():
			z.append(v)
		"""for data in fileMetadata:
			chunkIds.append(data[3])
		zipped_pairs = zip(chunkIds, data_retrieved)
		z = [x for _, x in sorted(zipped_pairs)]"""
		print(z)
		f=open("new"+fileName, "w")
		for data1 in z:
			f.write("%s\n" %data1)
		f.close()
		print(z)
