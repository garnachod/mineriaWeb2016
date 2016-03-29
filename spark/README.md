# INSTALACIÓN Apache Spark
## Instalar JAVA 8
* sudo apt-add-repository ppa:webupd8team/java
* sudo apt-get update
* sudo apt-get install oracle-java8-installer

## Instalar Spark (Tarda un buen rato, 20-40 minutos)
* wget http://apache.rediris.es/spark/spark-1.4.0/spark-1.4.0.tgz
* tar xvf spark-1.4.0.tgz
* cd spark-1.4.0
* sbt/sbt assembly

## Testeamos que todo haya salido bien
* ./bin/run-example SparkPi 10


## Variable del sistema
* sudo gedit /etc/profile
* export SPARK_HOME=/home/dani/spark/spark-1.4.0
* export PATH=$PATH:$SPARK_HOME