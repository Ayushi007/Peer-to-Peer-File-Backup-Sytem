#! /bin/sh

gcloud compute ssh $1 --command "cd src/; python3 $2"
