# Instalación (La una de la mañana)
* sudo su
* wget -O - http://debian.neo4j.org/neotechnology.gpg.key| apt-key add -
* echo 'deb http://debian.neo4j.org/repo stable/' > /etc/apt/sources.list.d/neo4j.list
* apt-get update -y
* apt-get install install neo4j
* pip install py2neo

## Pasos a continuacion
* Abrir el buscador
* http://localhost:7474
* te pedirá cambiar la contraseña
* Ya se puede usar si cambias la contraseña en Config/Conf.py

## Pintar el grafo
* MATCH (n) return n


## Problemas de rendimiento
* http://neo4j.com/docs/stable/performance-guide.html


## Ejemplo de visualización
![Alt text](../DesignImages/graph.png?raw=true "Diseño de clases")