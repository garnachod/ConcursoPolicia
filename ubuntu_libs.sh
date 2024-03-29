#!/bin/bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install linux-image-extra-`uname -r`
sudo apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install docker-engine
sudo apt-get install python-virtualenv
sudo apt-get install python-dev
sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran
sudo apt-get install libev4 libev-dev
sudo apt-get install libpq-dev