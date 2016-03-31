from LuigiTasks.GenerateSentimentTrain import GenerateTextByLang
from ProcesadoresTexto.Doc2Vec import Doc2Vec
from Config.Conf import Conf
import numpy as np
import luigi

class GenerateNLPByLang(luigi.Task):
	"""
	GenerateNLPByLang es la tarea que genera el modelo del texto
	Utiliza ProcesadoresTexto.Doc2Vec para crear los vectores de los tweets
	tiene como dependencia de tarea GenerateSentimentTrain.GenerateTextByLang
	"""

	lang = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%s.check'%(self.lang))

	def requires(self):
		return GenerateTextByLang(self.lang)
	
	def run(self):
		with self.output().open("w") as out:
			d2v = Doc2Vec()
			savePath = self.path.replace("check","model")

			conf = Conf()
			d2v.train(self.input().path, savePath, dimension = conf.getDimVectors(), epochs = 20, method="DBOW")
			out.write("OK")

class GenerateModelByLang(luigi.Task):
	"""
	GenerateModel crea el modelo de clasificacion de sentimientos. regresion lineal?
	"""	
	lang = luigi.Parameter()
	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%s.model'%(self.lang))

	def requires(self):
		return [GenerateTextByLang(self.lang), GenerateNLPByLang(self.lang)]
	
	def run(self):
		d2v = None
		modelLoc = ""
		ficheroTweets = None
		for input in self.input():
			if "check" in input.path:
				d2v = Doc2Vec()
				modelLoc = input.path.replace("check", "model")
			else:
				ficheroTweets = input.path

		lab = LabeledLineSentence(ficheroTweets, ides="String")
		Y = []
		x = []
		for tweet in lab:
			tag = tweet.tags
			if "POS" in tag[0]:
				Y.append(1)
			else:
				Y.append(0)

			vecX = d2v.simulateVectorsFromVectorText(tweet.words, modelLoc)
			X.append(vecX)

		Y = np.array(Y)
		X = np.array(X)


