from DBbridge.ConsultasCassandra import ConsultasCassandra
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


	def run(self):
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
		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsTextAndLang(self.lang)
		
		contadorPerTag = {"POS":0, "NEG":0, "NAN":0}

		for tweet in tweets:
			"TODO:"
			pass