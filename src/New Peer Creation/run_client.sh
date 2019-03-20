#! /bin/sh

gcloud compute ssh $1 --command "python3 $2"
