sudo docker network create --gateway 172.16.0.1 --subnet 172.16.0.0/21 mynet
sudo docker run --name cassandra1 --net=mynet --ip 172.16.0.2 --restart=always -d sharkcell/cassandra-stratio-lucene:3.0.6.2
sudo docker run --name cassandra2 --net=mynet --ip 172.16.0.5 --restart=always -d -e CASSANDRA_SEEDS=172.16.0.2 sharkcell/cassandra-stratio-lucene:3.0.6.2
sudo docker run --name postgres1 --net=mynet --ip 172.16.0.3 --restart=always -d postgres:latest
sudo docker run --name neo4j1 --net=mynet --ip 172.16.0.4 --restart=always --volume=$HOME/neo4j/data:/data -d neo4j:3.0
sudo iptables -t nat -A DOCKER -p tcp --dport 7474 -j DNAT --to-destination 172.16.0.4:7474
echo "EDIT neo4j password, open in your internet navigator ip:7474"
echo "THEN sudo iptables -D DOCKER 1 (that asume you don't have use other docker than these, if you use others delete the last iptable element, list: sudo iptables --line-numbers -L DOCKER)"
