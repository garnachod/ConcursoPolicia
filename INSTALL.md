#### ubuntu libs
* sudo ./ubuntu_libs.sh

#### Docker Servers
* sudo ./docker_deploy.sh
* Create 3 servers:
	* Cassandra: 172.16.0.2
	* PostgreSQL: 172.16.0.3
	* Neo4J: 172.16.0.4
 
##### Configuring Cassandra 
* sudo docker exec -it cassandra1 bash
* ./usr/bin/cqlsh
* CREATE KEYSPACE twitter WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
* exit from the docker

##### Configuring PostgreSQL
* sudo docker exec -it postgres1 bash
* su - postgres
* psql
* CREATE USER tfg WITH PASSWORD 'postgres_tfg';
* CREATE DATABASE twitter;
* CREATE DATABASE policia;
* GRANT ALL PRIVILEGES ON DATABASE twitter to tfg;
* GRANT ALL PRIVILEGES ON DATABASE policia to tfg;
* exit from the docker

###### Configuring Neo4j
* Open in your internet navigator {server_ip}:7474
* Change default Password
* for security:
	* sudo iptables --line-numbers -L DOCKER
	* sudo iptables -D DOCKER {the last number of the above instruccion}

#### Create Tables -> follow the PDF