#!/usr/bin/env bash
sudo docker network create --gateway 172.16.0.1 --subnet 172.16.0.0/21 mynet
sudo docker run --ulimit nofile=100000:100000 --ulimit nproc=32768:32768 --log-opt max-size=50m --name cassandra1 -v $HOME/cassandra1/data:/var/lib/cassandra -e MAX_HEAP_SIZE=8G -e HEAP_NEWSIZE=512M --net=mynet --ip 172.16.0.2 --restart=always -d cassandra:3
sudo docker run --ulimit nofile=100000:100000 --ulimit nproc=32768:32768 --log-opt max-size=50m --name cassandra2 -e CASSANDRA_SEEDS=172.16.0.2 -v $HOME/cassandra2/data:/var/lib/cassandra -e MAX_HEAP_SIZE=8G -e HEAP_NEWSIZE=512M --net=mynet --ip 172.16.0.5 --restart=always -d cassandra:3
sudo docker run --name postgres1 --net=mynet --ip 172.16.0.3 --restart=always -d postgres:latest
sudo docker run --name neo4j1 --net=mynet --ip 172.16.0.4 --restart=always --volume=$HOME/neo4j/data:/data -d neo4j:3.0
sudo iptables -t nat -A DOCKER -p tcp --dport 7474 -j DNAT --to-destination 172.16.0.4:7474
echo "EDIT neo4j password, open in your internet navigator ip:7474"
echo "THEN sudo iptables -D DOCKER 1 (that asume you don't have use other docker than these, if you use others delete the last iptable element, list: sudo iptables --line-numbers -L DOCKER)"
