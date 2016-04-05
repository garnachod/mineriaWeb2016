from LuigiTasks.GenerateSentimentTrain import GenerateTextByLang
from ProcesadoresTexto.Doc2Vec import Doc2Vec, LabeledLineSentence
from Config.Conf import Conf
import numpy as np
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from ProcesadoresTexto.SentimentalModel import SentimentalModel
from sklearn.externals import joblib
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
		return luigi.LocalTarget('%s/Data/%s.check'%(path, self.lang))

	def requires(self):
		return GenerateTextByLang(self.lang)
	
	def run(self):
		with self.output().open("w") as out:
			d2v = Doc2Vec()
			savePath = self.output().path.replace("check","model")

			conf = Conf()
			d2v.train(self.input().path, savePath, dimension = conf.getDimVectors(), epochs = 20, method="DBOW", isString=True)
			out.write("OK")

class GenerateModelByLang(luigi.Task):
	"""
	GenerateModel crea el modelo de clasificacion de sentimientos. regresion lineal?
	"""	
	lang = luigi.Parameter()
	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%s.mod_def'%(path, self.lang))

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
		X = []
		for tweet in lab:
			tag = tweet.tags
			if "POS" in tag[0]:
				Y.append(1)
				vecX = d2v.simulateVectorsFromVectorText(tweet.words, modelLoc)
				X.append(vecX)
			elif "NEG" in tag[0]:
				Y.append(-1)
				vecX = d2v.simulateVectorsFromVectorText(tweet.words, modelLoc)
				X.append(vecX)

			

		Y = np.array(Y)
		X = np.array(X)

		X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=42)

		logreg = linear_model.LogisticRegression(C=1e5)
		logreg.fit(X_train, y_train)

		# Explained variance score: 1 is perfect prediction
		print('Train score: %.2f' % logreg.score(X_train, y_train))
		print('Test score: %.2f' % logreg.score(X_test, y_test))

		tw_ejemplo = "carlos no es buena persona".split(" ")
		vecX = d2v.simulateVectorsFromVectorText(tw_ejemplo, modelLoc)

		print ('la clase predicha es: %d' % logreg.predict(vecX))

		with self.output().open("w") as fout:
			logreg_model_path = self.output().path.replace("mod_def", "logreg")
			senti = SentimentalModel.get_def(modelLoc, logreg_model_path, self.lang)
			fout.write(senti)
			joblib.dump(logreg, logreg_model_path)


