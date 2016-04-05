from ProcesadoresTexto.LimpiadorTweets import LimpiadorTweets
from ProcesadoresTexto.Doc2Vec import Doc2Vec, LabeledLineSentence
import numpy as np
import json

class SentimentalModel(object):
	"""sentimental model tiene como objetivo unificar el tratamiento 
		de los tweets o textos segun llegan sin tener que pasar por dos clases
		Sentimental model utiliza Doc2Vec para inferir el vector y el modelo de 
		clasificador para clasificarlo, asi como el lenguaje
	"""
	
	def __init__(self, model_location = None, is_lemat=False):
		super(SentimentalModel, self).__init__()
		#modelo doc2vec, genera los vectores.
		self.d2v = None
		#modelo regresion logistica, predice las clases
		self.logreg = None
		#lenguaje uno u otro ["es", "en"]
		self.lang = None

		#si la localizacion del modelo no es none
		if model_location is not None:
			self.load_def(location = model_location)




	def classifyMentions(self,tweets):
		"""
		Dada una mencion a una compania (array de Tweets),
		se realiza una clasificacion y nos devuelve su json
		para posteriormente pintarlo.
		"""
		results = {}

		#Realizamos una clasificacion de los Tweet de las menciones
		for tweet in tweets:
			result = self.classifyText(self,tweet)
			results[tweet] = result

		#Guardamos los resultados en un Json
		
		with open('results.txt', 'w') as outfile:
			json.dump(results, outfile)	

		return 


	def classifyText(self, text):
		"""Realiza la Clasificacion de un tweet mediante una 
		llamada a logreg.predict"""

		#Se procede a realizar el Preprocesado del Tweet
		vectX = self.Preprocesado(text)
		result = self.logreg.predict(vecX)

		print ('la clase predicha es: %d' % result)

		return result


	def load_def(self, location=None, string=None):
		"""
			carga el modelo desde una definicion json
			al menos tiene que tener un parametro distinto de None

			parametros de entrada:
				location: si no es None, es la localizacion en disco del JSON
				string: si no es None, es el modelo JSON sin parsear (json.parse())

			dentro de este json habra 3 variables:
				text_model: "localizacion en disco del modelo de texto en formato string"
				clasf_model: "localizacion en disco del modelo de clasificacion"
				lang: "lenguaje: solo puede ser (es, en)"

			estos modelos se han generado y guardado en LuigiTask/GenerateSentimentModel.py GenerateModelByLang
		"""

		#Comprobacion de los parametros de entrada
		if location is not None:
			#Lectura del fichero JSON dado por parametro
			with open(location) as data_file:    
				data = json.load(data_file)
		elif string is not None:
			#Realizamos el parseo del JSON  
				data = json.load(string)
		else:
			print "Parameters Error"
			return "ERR"

		#Modelo que nos genera los vectores
		self.d2v = data['text_model']
		#Almacenamos el modelo (regresion logistica)
		self.logreg = data['clasf_model']
		#Almacenamos el lenguaje
		self.lang = data['lang']

		return "OK"

	@staticmethod
	def get_def(d2v_loc, logreg_loc, lang):
		"""
			Para que la definicion del JSON y la lectura sea igual, lo metemos en la misma clase
			si nos fijamos en el @staticmethod, no tiene self

			genera y retorna un string JSON que dentro habra 3 variables:
				text_model: "localizacion en disco del modelo de texto en formato string"
				clasf_model: "localizacion en disco del modelo de clasificacion"
				lang: "lenguaje: solo puede ser (es, en)"


			la idea es que en LuigiTask/GenerateSentimentModel.py GenerateModelByLang se llame a este metodo
			para guardarlo con el formato bueno.
		"""

		#Escritura de las variabeles en un JSON String
		cadena_json = json.dumps({'text_model':d2v_loc, 'clasf_model':logreg_loc, 'lang':lang})
		#Retornamos el string que es json
		return cadena_json


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

		#Preprocesado del texto/Tweet
		tw_clean = self.clean(tweet)
		if len(tw_clean.split(" ")) <= 1:
			print "No se puede procesar el Tweet, ya que no contiene texto"
			return

		vecX = d2v.simulateVectorsFromVectorText(tw_clean, model)

		return vecX
