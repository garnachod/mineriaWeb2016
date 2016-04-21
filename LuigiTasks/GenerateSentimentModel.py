from LuigiTasks.GenerateSentimentTrain import GenerateTextByLang
from ProcesadoresTexto.Doc2Vec import Doc2Vec, LabeledLineSentence, Doc2Vec_sent
from Config.Conf import Conf
import numpy as np
from sklearn import linear_model
from sklearn.neural_network import MLPClassifier 
from sklearn.cross_validation import train_test_split
from ProcesadoresTexto.SentimentalModel import SentimentalModel
from sklearn.externals import joblib
import luigi
from sklearn.naive_bayes import GaussianNB

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
			d2v.train(self.input().path, savePath, dimension = conf.getDimVectors(), epochs = 20, method="DM", isString=True)
			out.write("OK")

class GenerateNLPByLang_research(luigi.Task):
	"""
	GenerateNLPByLang es la tarea que genera el modelo del texto
	Utiliza ProcesadoresTexto.Doc2Vec_sent para crear los vectores de los tweets
	tiene como dependencia de tarea GenerateSentimentTrain.GenerateTextByLang
	"""
	lang = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%srs.check'%(path, self.lang))

	def requires(self):
		return GenerateTextByLang(self.lang)
	
	def run(self):
		with self.output().open("w") as out:
			d2v = Doc2Vec_sent()
			savePath = self.output().path.replace("check","model")

			conf = Conf()
			d2v.train(self.input().path, savePath, dimension = conf.getDimVectors(), epochs = 20, method="DM", isString=True)
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

	def train(self, X_train, y_train):
		logreg = linear_model.LogisticRegression(C=1e5)
		logreg.fit(X_train, y_train)
		return logreg

	def test(self, d2v, d2v_loc, model):
		tw_ejemplo = "no me gusta nada esta empresa porque mata gente".split(" ")
		vecX = d2v.simulateVectorsFromVectorText(tw_ejemplo, d2v_loc)

		print ('la clase predicha es: %d' % model.predict([vecX]))
	
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

		clf = self.train(X_train, y_train)

		# Explained variance score: 1 is perfect prediction
		print('Train score: %.5f' % clf.score(X_train, y_train))
		print('Test score: %.5f' % clf.score(X_test, y_test))

		self.test(d2v, modelLoc, clf)

		with self.output().open("w") as fout:
			sk_model_path = self.output().path.replace("mod_def", "sklearn")
			senti = SentimentalModel.get_def(modelLoc, sk_model_path, self.lang)
			fout.write(senti)
			joblib.dump(clf, sk_model_path)


class GenerateModelByLang_MLP(GenerateModelByLang):
	"""docstring for GenerateModelByLang_MLP"""

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%sMLP.mod_def'%(path, self.lang))
	
	def train(self, X_train, y_train):
		clf = MLPClassifier(algorithm='adam', alpha=1e-5, hidden_layer_sizes=(25,10), random_state=1, activation='logistic')
		clf.fit(X_train, y_train)
		return clf

class GenerateModelByLang_MLP_rs(GenerateModelByLang_MLP):
	"""docstring for GenerateModelByLang_MLP"""

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%sMLP_rs.mod_def'%(path, self.lang))

	def requires(self):
		return [GenerateTextByLang(self.lang), GenerateNLPByLang_research(self.lang)]
	
	

class GenerateModelByLang_Naive(GenerateModelByLang):
	"""docstring for GenerateModelByLang_Naive_Bayes"""

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%sNaive_Bayes.mod_def'%(path, self.lang))
	
	def train(self, X_train, y_train):
		clf = GaussianNB()
		clf.fit(X_train, y_train)
		return clf

class GenerateModelByLang_Naive_rs(GenerateModelByLang_Naive):
	"""docstring for GenerateModelByLang_Naive"""

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%sNaive_rs.mod_def'%(path, self.lang))

	def requires(self):
		return [GenerateTextByLang(self.lang), GenerateNLPByLang_research(self.lang)]

class GenerateModelByLang_rs(GenerateModelByLang):
	"""docstring for GenerateModelByLang"""

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/%s_rs.mod_def'%(path, self.lang))

	def requires(self):
		return [GenerateTextByLang(self.lang), GenerateNLPByLang_research(self.lang)]