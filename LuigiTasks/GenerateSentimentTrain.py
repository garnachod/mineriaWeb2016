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
	limite_balanceo = luigi.IntParameter(default=100000)

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%s.train'%(path, self.lang), format=luigi.format.TextFormat(encoding='utf8'))


	def run(self):
		"""
		Ejecucion:

		se puede utilizar getTweetsTextAndLang en ConsultasCassandra,
		por cada tweet comprobar el sentimiento, si es que tiene.
		se pueden almacenar tweets en el idioma dado pero que no contengan sentimiento 
		esto mejora el procesamiento de texto.
		"""
		"""
		http://incc-tps.googlecode.com/svn/trunk/TPFinal/bibliografia/Pak%20and%20Paroubek%20(2010).%20Twitter%20as%20a%20Corpus%20for%20Sentiment%20Analysis%20and%20Opinion%20Mining.pdf
		"""
		Happy_emoticons = [":-)",":)", "=)",":D",";)"] #Emoticonos de positividad
		Sad_emoticons = [":-(",":(","=(",";("] #Emoticonos negatividad

		#Consultas a la base de datos 
		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsTextAndLang(self.lang, limit = 50000000)
		
		#Contadores para cada tag 
		contadorPerTag = {"POS":0, "NEG":0, "NAN":0}

		with self.output().open('w') as outfile:
			for tweet in tweets:
				if contadorPerTag['NEG'] >= self.limite_balanceo and contadorPerTag['POS'] >= self.limite_balanceo:
					#si se ha llegado a los dos limites no hace falta que sigamos computando
					break

				tw_clean = self.clean(tweet)
				if len(tw_clean.split(" ")) <= 1:
					continue

				flag = False 
				if contadorPerTag['POS'] <= self.limite_balanceo:
					for icon in Happy_emoticons:
						if icon in tweet[0]:
							#escritura de la etiqueta
							outfile.write(u"POS_%d\n" % contadorPerTag['POS'])
							#escritura del tweet
							outfile.write(u"%s\n"% tw_clean)
							#se aumenta el contador de elementos positivos
							contadorPerTag['POS']+=1
							flag = True
							break


				if contadorPerTag['NEG'] <= self.limite_balanceo and flag == False:
					for icon in Sad_emoticons:
						if icon in tweet[0]:
							#escritura de la etiqueta
							outfile.write(u"NEG_%d\n" % contadorPerTag['NEG'])
							#escritura del tweet
							outfile.write(u"%s\n"% tw_clean)
							#se aumenta el contador de elementos negativos
							contadorPerTag['NEG'] += 1
							flag = True
							break

				if flag == False and contadorPerTag['NAN'] < 1000000:
					#escritura de la etiqueta
					outfile.write(u"NAN_%d\n" % contadorPerTag['NAN'])
					#escritura del tweet
					outfile.write(u"%s\n"% tw_clean)
					#se aumenta el contador de elementos negativos
					contadorPerTag['NAN'] += 1

				


	def clean(self,tweet):	
		"""
		Realiza llamadas a la funcion que limpia Tweets para
		a continuacion poder procesarlos.
		"""	
		#Procesado de los Tweets
		tweetLimpio = LimpiadorTweets.clean(tweet.status)
		tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)

		return tweetSinStopWords