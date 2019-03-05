#! /bin/sh

gcloud compute firewall-rules create --network=NETWORK           \
        default-allow-ssh --allow tcp:22
gcloud compute ssh $1 --command "mkdir src; cd src/; exit"
gcloud compute scp $2 $1:src/
