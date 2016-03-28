from django.db import models

class Tarea(models.Model):
	"""
	Tarea, clase que define las tareas almacenadas
	No hay usuarios de la aplicacion

	Tipo define el tipo de tarea:
		SentimentsByUser, SentimentsByMentions

	username:
		usuario de twitter

	idioma:
		idioma de los tweets que analizaremos

	inicio:
		fecha y tiempo de inicio para ordenar las tareas
		
	"""
	tipo = models.CharField(max_length=100)
	username = models.CharField(max_length=20)
	idioma = models.CharField(max_length=2)
	inicio = models.DateTimeField()