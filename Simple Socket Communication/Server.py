#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python3

import socket

HOST = '172.20.10.3'  # Standard loopback interface address (localhost)
PORT = 8888       # Port to listen on (non-privileged ports are > 1023)


# In[2]:


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print ("Hello", s.accept())
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


# In[ ]:




