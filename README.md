# BACKpackers
## Peer to Peer Backup System
Virtual machine instances can be created on google cloud or localhost. 
We have automated the peer creation in google cloud.
The tracker is assumed to be up and running always in our system. The role of the tracker is to remain connected to all the peers in the network and allow new peer addition to the network.
With each peer in the network, it will execute source (peer.py) code and will display menu for user input.
The menu will have options to either backup a local file or retrieve an already backed up file. 

### Dependencies
* Python 3.0 or higher
* Gcloud CLI
* OS: Ubuntu 16.04

### Setting up Gcloud CLI
1. Install Google Cloud SDK
```
sudo apt-get update && sudo apt-get install google-cloud-sdk
```
2. Initialize gcloud CLI
```
gcloud init
```

### Running the system
#### On Google Clould Platform
##### Setting up Tracker
1. Create an instance called `Tracker`
```
python3 create_peer.py [Tracker]
```
2. Push Tracker code into the instance
```
./push_file.sh Tracker tracker.py

```
3. Run Tracker
```
python3 tracker.py
```

##### Creating new Peer
```
python3 create_peer.py [Peer Name]
```
##### Pushing files into Peer
```
./push_file.sh [Peer Name] [File]
```
#### On LAN 
##### Setting up Tracker
1. Copy `tracker.py` from [src/Tracker/](https://github.com/ecs251-w19-ucdavis/BACKpackers/tree/master/src/Tracker) and paste it into a system.
2. Run Tracker
```
python3 tracker.py
```

##### Adding new Peers to Network
1. Copy `peer.py` and `divideFile.py` from [src/Peer1](https://github.com/ecs251-w19-ucdavis/BACKpackers/tree/master/src/Peer1) and paste it into a system in the network.
2. Run peer code
```
python3 peer.py
```

### Perform Backup
1. Enter `1` as option in menu
```
Menu:
1. Backup
2. Retrieve
List your choice: 1
```
2. Choose file to Back up 
```
Enter the filename: [File Name]
```
3. Choose priority of File
```
1. High Priority File (3 copies will be created)
2. Low Priority File (2 copies will be created)
List your choice: [1 or 2]
```
### Perform Retrieval
1. Enter `2` as option in menu
```
Menu:
1. Backup
2. Retrieve
List your choice: 2
```
2. Choose file to Retrieve
```
Enter the file name: [File Name]
```

