from Config.Conf import Conf
import luigi

class GenerateNLPByLang(luigi.Task):
	"""
	GenerateNLPByLang es la tarea que genera el modelo del texto
	Utiliza ProcesadoresTexto.Doc2Vec para crear los vectores de los tweets
	tiene como dependencia de tarea GenerateSentmentTrain.GenerateTextByLang
	"""

class SentimentalModel(object):
	"""Mover a procesadores de texto?????"""


	"""sentimental model tiene como objetivo unificar el tratamiento 
		de los tweets o textos segun llegan sin tener que pasar por dos clases
		Sentimental model utiliza Doc2Vec para inferir el vector y el modelo de 
		clasificador para clasificarlo
	"""
	def __init__(self, arg):
		super(SentimentalModel, self).__init__()

	def train():
		pass

	def load_def():
		"""
			carga el modelo desde una definicion json
		"""
		pass

	def get_def():
		"""
			retorna en formato json la definicion del modelo
		"""

	


class GenerateModel(luigi.Task):
	"""
	GenerateModel crea el modelo de clasificacion de sentimientos. regresion lineal?
	"""	