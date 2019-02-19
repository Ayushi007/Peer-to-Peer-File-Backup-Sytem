# Group1
Peer to Peer Backup System

# Week 1 Notes

## Progress

### 1. Reviewed existing implementations of BitTorrent and BlackBox
Most of the implementations were in shell scripting and we were looking for something in python or C++

### 2.  Tried to implement basic Peer-2-Peer backup system in python
In this implementation we created one client which back up the file chunk and a tracker to keep track of the information about the chunks and where these chunks are. The peers communicate with the tracker requesting the required information. We have created a master peer which requests for the chunks and combine them to recreate the complete file. But, in the end we are getting error in master peer while retrieving the chunks.

### 3. Tried BitTorrent implementation in C++
We tried understanding and implementing the code for P2P backup system using BitTorrent method, but we facing issues related to some header files (like peer.h) not available in the source code file.

## Next Week Plans
We plan to build a basic P2P system from scratch and for that we will design the network and setup nodes in the initial phase. We plan to establish communication sockets among them and send files over them before the next meeting. For simplicity, these files for now will not be encrypted or encoded. 


