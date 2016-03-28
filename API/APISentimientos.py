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
		return pos, neg

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
		return pos, neg

	def isTaskFinished(username, lang, tipo_tarea):
		"""
		comprueba si una tarea esta terminada o no
		Al ser por debajo tareas luigi, comprueba si el fichero existe

		Parameters
		----------
		username : usuario de la red social con @ o sin @
		lang : lenguaje de los usuarios a analizar
		tipo_tarea : SentimentsByUser o SentimentsByMentions
		
		Returns
		-------
		True si tarea terminada, False si no
		"""
		pass