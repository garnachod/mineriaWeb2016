from DBbridge.ConsultasCassandra import ConsultasCassandra
from ProcesadoresTexto.LimpiadorTweets import LimpiadorTweets
from Config.Conf import Conf
import luigi


class GenerateTextByLang(luigi.Task):
	"""
		GenerateTextByLang

	genera un fichero de texto con los tweets con un sentimiento definido (positivo o negativo)
	en un lenguaje dado
	El formato de salida es:
	0 SENTIMIENTO_identificadorunico
	1 texto tweet

	0 y 1 son el numero de linea, por lo que las lineas pares contienen la etiqueta
	y las lineas impares contienen texto.

	El sentimiento puede ser POS, NEG o NAN (si no lo hemos identificado)
	"""
	lang = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%s.train'%(self.lang))


	def run(self,limite_balanceo):		
		"""
		Ejecucion:

		se puede utilizar getTweetsTextAndLang en ConsultasCassandra,
		por cada tweet comprobar el sentimiento, si es que tiene.
		se pueden almacenar tweets en el idioma dado pero que no contengan sentimiento 
		esto mejora el procesamiento de texto.
		"""

		"""
		Por otro lado para procesar el texto, ProcesadoresTexto.LimpiadorTweets contiene todo.
		"""
		Happy_emoticons = [":-)",":)", "=)",":D",";)"]   #Emoticonos de positividad
		Sad_emoticons = [":-(",":(","=(",";("]	#Emoticonos negatividad
		ID = 0 #ID unico para cada Tweet
		outfile = open('sentimentalTweets.csv', 'w') #Fichero de salida

		#Consultas a la base de datos 
		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsTextAndLang(self.lang)

		#Procesado de los Tweets
		limpiarT = LimpiadorTweets()
		
		#Contadores para cada tag 
		contadorPerTag = {"POS":0, "NEG":0, "NAN":0}

		for tweet in tweets:
			if contadorPerTag['POS'] <= limite_balanceo:
				for icon in Happy_emoticons:
					if icon in tweet[0]:
						outfile.write("0 POSITIVO_%d;" % ID)
						cl = clean(self,tweet[0])
						outfile.write("1 %s\n" % cl)
						ID+=1
						contadorPerTag['POS']+=1
						break
			elif contadorPerTag['NEG'] <= limite_balanceo:
				for icon in Sad_emoticons:
					if icon in tweet[0]:
						outfile.write("0 NEGATIVO_%d;" % ID)
						cl = clean(self,tweet[0])
						outfile.write("1 %s\n" % cl)
						ID+=1
						contadorPerTag['NEG']+=1
						break

		#Cerramos el fichero de texto
		outfile.close() 
		return 

	def clean(self,tweet):	
		"""
		Realiza llamadas a la función que limpia Tweets para
		a continuación poder procesarlos.
		"""	
		#Procesado de los Tweets
		limpiarT = LimpiadorTweets()

		cleaned = limpiarT.clean(tweet)

		cleaned = stopWordsByLanguagefilter(cleaned,self.lang)

		cleaned = stemmingByLanguage(cleaned,self.lang)

		return cleaned