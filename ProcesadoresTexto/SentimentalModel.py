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
	def __init__(self, text_Model_Location, lang, is_lemat):
		super(SentimentalModel, self).__init__()


	def classifyMentions(self,tweets):
		"""
		Dada una mencion a una compañía (array de Tweets),
		se realiza una clasificación y nos devuelve su json
		para posteriormente pintarlo.
		"""
		results = {}

		#Realizamos una clasificación de los Tweet de las menciones
		for tweet in tweets:
			result = self.classifyText(self,tweet)
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

		#Primero Cargamos y obtenemos el modelo
		self.load_def(self)
		modelLoc = self.get_def(self)

		Y = []
		X = []
		for tweet in lab:
			tag = tweet.tags
			if "POS" in tag[0]:
				Y.append(1)
			elif "NEG" in tag[0]:
				Y.append(0)

			vecX = d2v.simulateVectorsFromVectorText(tweet.words, modelLoc)
			X.append(vecX)

		Y = np.array(Y)
		X = np.array(X)

		X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=42)

		logreg = linear_model.LogisticRegression(C=1e5)
		logreg.fit(X_train, y_train)

		#Se procede a realizar el Preprocesado del Tweet
		vectX = Preprocesado(self,text,modelLoc)

		result = logreg.predict(vecX)

		print ('la clase predicha es: %d' % result)

		return result


	def load_def(self, location=None, string=None):
		"""
			carga el modelo desde una definicion json
			al menos tiene que tener un parametro distinto de None
		"""

		d2v = None
		modelLoc = ""
		ficheroTweets = None


		for input in location:
			if "check" in input.path:
				d2v = Doc2Vec()
				modelLoc = location.replace("check", "model")
			else:
				ficheroTweets = location

		lab = LabeledLineSentence(ficheroTweets,string)

		return

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

		#Preprocesado del texto/Tweet
		tw_clean = self.clean(tweet)
		if len(tw_clean.split(" ")) <= 1:
			print "No se puede procesar el Tweet, ya que no contiene texto"
			return

		vecX = d2v.simulateVectorsFromVectorText(tw_clean, model)

		return vecX
