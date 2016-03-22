##### instalar
http://docs.datastax.com/en/getting_started/doc/getting_started/gettingStartedDeb_t.html

sudo apt-get install cassandra=2.1.8

##### instalar blist y cassandra-driver para python
* sudo pip install blist
* sudo pip install cassandra-driver

##### Instalar lucene-cassandra
* GIT https://github.com/Stratio/cassandra-lucene-index
* CASSANDRA_HOME == /usr/share/cassandra

##### arrancar la interfaz de cassandra para crear el keyspace
```
 cd /usr/bin/
 ./cqlsh
 CREATE KEYSPACE twitter WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
 CREATE KEYSPACE instagram WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
```

##### ya se pueden crear las "tablas"
* utilizar el fichero CreaTablas.py

#### Solución de problemas
##### Cassandra no arranca por problemas en librerias o datos
* dani@dani-GA-890XA-UD3:/var/lib/cassandra$ sudo service cassandra stop
* dani@dani-GA-890XA-UD3:/var/lib/cassandra$ sudo rm -rf ./data/*
* dani@dani-GA-890XA-UD3:/var/lib/cassandra$ sudo rm -rf ./commitlog/*
* dani@dani-GA-890XA-UD3:/var/lib/cassandra$ sudo rm -rf ./saved_caches/*
* dani@dani-GA-890XA-UD3:/var/lib/cassandra$ sudo service cassandra start

##### Timeout de escritura
* dani@dani-GA-890XA-UD3:/etc/cassandra$ sudo gedit cassandra.yaml
* (EDITAR) write_request_timeout_in_ms: 20000
