from DBbridge.ConsultasCassandra import ConsultasCassandra
from LuigiTasks.RecolectorTwitter import RecolectorContenidoTweet
from LuigiTasks.GenerateSentimentModel import GenerateModelByLang
from Config.Conf import Conf
import luigi

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
		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsTopicsCassandra(self.user, limit=10000)
		tweetsStatus = []
		for tweet in tweets:
			if tweet.lang == self.lang:
				tweetsStatus.apend(tweet.status)

		