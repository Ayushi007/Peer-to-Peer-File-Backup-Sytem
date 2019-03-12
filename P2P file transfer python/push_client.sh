#! /bin/sh

gcloud compute ssh $1 --command "mkdir src; cd src/; exit"
gcloud compute scp $2 $1:src/
