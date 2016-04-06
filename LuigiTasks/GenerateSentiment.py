from DBbridge.ConsultasCassandra import ConsultasCassandra
from LuigiTasks.RecolectorTwitter import RecolectorContenidoTweet
from LuigiTasks.GenerateSentimentModel import GenerateModelByLang
from ProcesadoresTexto.SentimentalModel import SentimentalModel
from Config.Conf import Conf
import luigi
import json

class GenerateSentimentMetions(luigi.Task):
	lang = luigi.Parameter()
	user = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		return luigi.LocalTarget('%s/Data/results/%s.%s.json'%(path, self.lang, self.user))
	
	def requires(self):
		if "#" in self.user:
			self.user = self.user.replace("#", "")
		return [RecolectorContenidoTweet(busqueda=self.user, limitedescarga="10000"), GenerateModelByLang(lang=self.lang)]

	def run(self):
		sentimentModel = None
		for input in self.input():
			if "mod_def" in input.path:
				sentimentModel = SentimentalModel(model_location = input.path)

		consultas = ConsultasCassandra()
		tweets = consultas.getStatusTopicsCassandra(self.user, limit=10000)
		tweets_in = []
		for tweet in tweets:
			if tweet.lang == self.lang:
				tweets_in.append(tweet)

		sents = sentimentModel.classifyMentions(tweets_in)

		sentsOut =  {"pos" : sents["1"], "neg" : sents["-1"]}
		with self.output().open("w") as outfile:
			strSentsOut = json.dumps(sentsOut)
			outfile.write(strSentsOut)
		
class GenerateSentimentUser(luigi.Task):
	"""docstring for GenerateSentimentUser"""
	pass
		