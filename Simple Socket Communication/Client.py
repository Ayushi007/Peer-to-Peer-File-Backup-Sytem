#!/usr/bin/env python
# coding: utf-8

# In[3]:


#!/usr/bin/env python3

import socket

HOST = '172.20.10.5'  # The server's hostname or IP address
PORT= 8888         # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print("done sending")
print('Received', repr(data))


# In[ ]:




