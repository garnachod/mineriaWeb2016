from LuigiTasks.GenerateSentimentTrain import GenerateTextByLang
from ProcesadoresTexto.Doc2Vec import Doc2Vec
from Config.Conf import Conf
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
		return luigi.LocalTarget('%s/Data/%s.d2v'%(self.lang))

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
		pass