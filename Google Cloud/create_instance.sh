#! /bin/sh
gcloud compute instances create $1 \
--image-family ubuntu-1804-lts \
--image-project gce-uefi-images \
> $1.txt
