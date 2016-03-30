class SentimentalModel(object):
	"""Mover a procesadores de texto?????"""


	"""sentimental model tiene como objetivo unificar el tratamiento 
		de los tweets o textos segun llegan sin tener que pasar por dos clases
		Sentimental model utiliza Doc2Vec para inferir el vector y el modelo de 
		clasificador para clasificarlo, asi como el lenguaje
	"""
	def __init__(self, text_Model_Location, lang, is_lemat):
		super(SentimentalModel, self).__init__()

	def train(self):
		pass

	def classifyText(self, text):
		"""
		dado un texto sin procesar
		"""
		pass
	def load_def(self, location=None, string=None):
		"""
			carga el modelo desde una definicion json
			al menos tiene que tener un parametro distinto de None
		"""
		pass

	def get_def(self):
		"""
			retorna en formato json string la definicion del modelo
		"""
