# Week 1 Notes

## Last Week’s Updates & Related Issues 

### 1. Reviewed existing implementations of BitTorrent and BlackBox
Everyone - Most of the implementations were in shell scripting and we were looking for something in python or C++, that we could understand easily and manipulate but we could not find a lot of those. 

### 2. Attempt 1 - BitTorrent implementation in C++
Ayushi - In this implementation, we tried to understand and implement one of the existing implementation of P2P backup system using BitTorrent approach in C++, but we faced some issues related to some header files (ex. peer.h & JSON.h) which were not available in the source code folder, while we were able to figure JSON.h which was more of the standard one, we could not find out the specific peer.h file used. 

### 3. Attempt 2 - Implement basic Peer-2-Peer backup system in python
Mridula - In the next implementation, we tried to create one client which backs up the file chunk, and a tracker to keep track of the chunks information and their location. The peers communicate with the tracker requesting the required information. We have created a master node which requests for the chunks and combine them to recreate the complete file. But, in the end we are getting some error in master peer while retrieving the chunks, we are hoping to make it work or may be solve this with a different approach

## This Week Plans
1. We plan to create peers by creating virtual machines on cloud using google cloud platform or any other available open source software.
2. Then, similar to file transfer methods used in our previous implementations of this week, we will build P2P system from scratch
3. We will establish communication sockets among the peers and will be able to send and receive files over them before the next meeting. For simplicity, these files for now will not be encrypted or encoded.


## Link to Trello - 
https://trello.com/b/lABFR50h/os-project
    
