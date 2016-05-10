# Proyecto Minería Web 2016
Proyecto

## siempre antes de comenzar a trabajar Activar Virtual Enviroment
source venv/bin/activate

## al cambiar el código de una librería con el venv activo
python setup.py install

## ejemplo del ejecucion de Luigi
* luigi --module LuigiTasks.GenerateSentimenTrain GenerateTextByLang --lang es

### WorkFlow:
* Se lanza una búsqueda en la web, se permite insertar un usuario de Twitter y el idioma del analisis
* Si la tarea no esta computada se informa al usuario y se añade a tareas
* Si la tarea esta computada se muestran los resultados en la interfaz


## Sentimental analysis using Doc2Vec (Paragraph Vector)


### Papers del proyecto
* [Paragraph Vector](https://cs.stanford.edu/~quocle/paragraph_vector.pdf)
* [Twitter as a Corpus for Sentiment Analysis and Opinion Mining.](http://incc-tps.googlecode.com/svn/trunk/TPFinal/bibliografia/Pak%20and%20Paroubek%20(2010).%20Twitter%20as%20a%20Corpus%20for%20Sentiment%20Analysis%20and%20Opinion%20Mining.pdf)
* [Paragraph vector + LSTMs](https://cs224d.stanford.edu/reports/HongJames.pdf)


### Librería de procesamiento de lenguaje natural
* https://radimrehurek.com/gensim/
