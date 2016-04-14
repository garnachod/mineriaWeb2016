import os
import luigi
from LuigiTasks.GenerateSentiment import GenerateSentimentMetions, GenerateSentimentUser
from DBbridge.ConsultasCassandra import ConsultasCassandra

from Config.Conf import Conf
import json
import re

import multiprocessing

re_tuser = re.compile(r'@?[a-zA-Z0-9_]+')


class _generateSentiment(multiprocessing.Process):
	"""docstring for _generateSentiment"""
	def __init__(self, lang, username, mentions):
		super(_generateSentiment, self).__init__()
		self.lang = lang
		self.mentions = mentions
		self.username = username

	def run(self):
		#configuracion del sistema
		conf = Conf()
		path = conf.getAbsPath()
		comand = "luigi --module LuigiTasks.GenerateSentiment "
		if self.mentions == True:
			comand += "GenerateSentimentMetions"
		else:
			comand += "GenerateSentimentUser"
		comand += " --lang " + self.lang + "  --user " + self.username
		comand += " > /dev/null 2>&1"
		
		os.popen(comand)

class APISentimientos(object):
	"""APISentimientos, operaciones permitidas en la api relativa a los sentimientos"""

	@staticmethod
	def getSentimentsByMentions(username, lang):
		"""
		Calcula y retorna en valor absoluto el numero 
		de sentimientos positivos y negativos en las menciones 
		que se han realizado a una cuenta de twitter.

		Parameters
		----------
		username : usuario de la red social con @ o sin @
		lang : lenguaje de los usuarios a analizar
		
		Returns
		-------
		#sentimientos positivos, #sentimientos negativos
		"""
		pos = 0
		neg = 0

		is_finish = APISentimientos.isTaskFinished(username, lang,"SentimentsByMentions")
		
		if is_finish == False:
			return False
		
		#Lectura del JSON que nos dice los sentimientos de los usuarios
		with open(is_finish) as data_file:    
			data = json.load(data_file)

		#Cargamos el numero de positivos y negativos
		pos = data["pos"]
		neg = data["neg"]

		return pos, neg

	@staticmethod
	def getSentimentsByUser(username, lang):
		"""
		Calcula y retorna en valor absoluto el numero 
		de sentimientos positivos y negativos en la cuenta 
		a analizar de twitter.

		Parameters
		----------
		username : usuario de la red social con @ o sin @
		lang : lenguaje de los usuarios a analizar
		
		Returns
		-------
		#sentimientos positivos, #sentimientos negativos
		"""
		pos = 0
		neg = 0

		is_finish = APISentimientos.isTaskFinished(username, lang,"SentimentsByUser")
		
		if is_finish == False:
			return False

		#Lectura del JSON que nos dice los sentimientos de los usuarios
		with open(is_finish) as data_file:    
			data = json.load(data_file)

		#Cargamos el numero de positivos y negativos
		pos = data["pos"]
		neg = data["neg"]

		return pos, neg

	@staticmethod
	def isTaskFinished(username, lang, tipo_tarea, download=True):
		"""
		comprueba si una tarea esta terminada o no
		Al ser por debajo tareas luigi, comprueba si el fichero existe

		Parameters
		----------
		username : usuario de la red social con @ o sin @
		lang : lenguaje de los usuarios a analizar
		tipo_tarea : SentimentsByUser o SentimentsByMentions
		download : si true, si no esta el fichero, lanza la tarea, si false no lo crea
		
		Returns
		-------
		True si tarea terminada, False si no
		"""

		if len(username) > 16 or len(username) < 2 or re_tuser.match(username) == None:
			raise Exception("Parametros incorrectos")

		if lang != 'es' and lang != 'en':
			raise Exception("Parametros incorrectos")

		if tipo_tarea == "SentimentsByMentions":
			sentiment = GenerateSentimentMetions(lang = lang, user = username)

			#Comprobamos si existe el JSON que nos define a dicho usuario
			if os.path.isfile(sentiment.output().path) == False:
				if download:
					p = _generateSentiment(lang, username, True)
					p.start()
				return False
			else:
				return sentiment.output().path
		else:
			sentiment = GenerateSentimentUser(lang = lang, user = username)

			#Comprobamos si existe el JSON que nos define a dicho usuario
			if os.path.isfile(sentiment.output().path) == False:
				if download:
					p = _generateSentiment(lang, username, False)
					p.start()
				return False
			else:
				return sentiment.output().path

		