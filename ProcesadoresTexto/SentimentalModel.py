from ProcesadoresTexto.LimpiadorTweets import LimpiadorTweets
from ProcesadoresTexto.Doc2Vec import Doc2Vec, LabeledLineSentence
import numpy as np
import json

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


		###NO ENTIENDO: SERÍA UNA LLAMADA AL FICHERO DE TRAIN NO???

		pass



	def classifyMentions(self,tweets):
		"""
		Dada una mencion a una compañía (array de Tweets),
		se realiza una clasificación y nos devuelve su json
		para posteriormente pintarlo.
		"""
		results = {}

		#Realizamos una clasificación de los Tweet de las menciones
		for tweet in tweets:
			result = classifyText(self,tweet)
			results[tweet] = result

		#Guardamos los resultados en un Json
		with open('results.txt', 'w') as outfile:
    		json.dump(results, outfile)	

		return 


	def classifyText(self, text):
		"""
		Dado un texto sin procesar realizamos la clasificación
		del Tweet
		"""
		modelLoc = ""
		X = []

		#Primero Cargamos y obtenemos el modelo
		load_def(self)
		modelLoc = get_def(self)

		#Se procede a realizar el Preprocesado del Tweet
		X = Preprocesado(self,text,modelLoc)



		pass
	def load_def(self, location=None, string=None):
		"""
			carga el modelo desde una definicion json
			al menos tiene que tener un parametro distinto de None
		"""

		###NO ENTIENDO DESDE UN JSON???
		pass

	def get_def(self):
		"""
			retorna en formato json string la definicion del modelo
		"""

		###NO ENTIENDO DESDE UN JSON???

	def clean(self,tweet):	
		"""
		Realiza llamadas a la funcion que limpia Tweets para
		a continuacion poder procesarlos.
		"""	
		#Procesado de los Tweets
		tweetLimpio = LimpiadorTweets.clean(tweet.status)
		tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)

		return tweetSinStopWords

	def Preprocesado(self,tweet,model):
		"""
		Realiza el preprocesado de los Tweets y los convierte en 
		un array de palabras.
		"""	

		X = []

		#Preprocesado del texto/Tweet
		tw_clean = self.clean(tweet)
		if len(tw_clean.split(" ")) <= 1:
			print "No se puede procesar el Tweet, ya que no contiene texto"
			return

		vecX = d2v.simulateVectorsFromVectorText(tw_clean, model)

		X.append(vecX)

		X = np.array(X)

		return X
