# Proyecto Minería Web 2016
Proyecto

## siempre antes de comenzar a trabajar Activar Virtual Enviroment
source venv/bin/activate

## al cambiar el código de una librería con el venv activo
python setup.py install

### TO DO:
* API/APISentimientos.py (Llenar de código)
* website/mineria/models.py (Carlos enterarte del modelo de tareas)
* LuigiTasks/GenerateSentimenTrain.py (Llenar de código) (Dani o Carlos al menos definir clases)
* LuigiTasks/GenerateSentimentModel.py (Llenar de  código) (Dani o Carlos al menos definir clases)
* LuigiTasks/GenerateSentiment.py (lo mismo)
* UI -> Añadir desplegable de idiomas permitidos

### WorkFlow:
* Se lanza una búsqueda en la web, se permite insertar un usuario de Twitter y el idioma del analisis
* Si la tarea no esta computada se informa al usuario y se añade a tareas
* Si la tarea esta computada se muestran los resultados en la interfaz


## Sentimental analysis using Word2Vec (Paragraph Vector)
https://cs.stanford.edu/~quocle/paragraph_vector.pdf

https://radimrehurek.com/gensim/

## Instrucciones de instalación desde 0 (No hacer Carlos)
* Instalar Cassandra: probado con Cassandra 2.1.11
	* Podía funcionar 2.1.13 sin cambiar nada
	* Podría funciona con otras versiones de Cassandra pero seguramente cambie alguna consulta
	* Crear keyspace twitter
* Instalar Neo4J: no hay problemas con la versión por ahora
	* Configurar la contraseña, si no cambiamos la de por defecto falla
* Instalar PostgreSQL
	* Crear dos Bases de datos (policia, twitter)
* Instalar https://github.com/Stratio/cassandra-lucene-index instalar la misma version que Cassandra
* Copiar Config/Conf_default.py con el nombre de Conf.py
	* Configurar los parametros correctos.
* Instalar las librerias de las que se compone el proyecto:
	* sudo python setup.py install
	* remove:
	* python setup.py install --record files.txt
	* cat files.txt | xargs rm -rf
* Lanzar creación de tablas:
	* DBbridge/Cassandra/Creatablas.py
	* DBbridge/Neo4j/CreaRelaciones.py
	* DBbridge/PostgreSQL/CreaTablas.py
* Instalar las librerías python:
	* Instalar dependencias con pip install -r requirements.txt
	* Creat tablas de Django con python manage.py migrate
* Configurar cronjobs
* Si Luigi se va a lanzar desde apache:
	* chown -R www-data:www-data LuigiTasks/