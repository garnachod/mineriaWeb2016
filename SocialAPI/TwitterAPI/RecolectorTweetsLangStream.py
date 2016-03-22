# -*- coding: utf-8 -*-
import os
import sys
#lib_path = os.path.abspath('../../')
#sys.path.append(lib_path)
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra

from SocialAPI.Recolector import Recolector
from twython import TwythonStreamer
from ApoyoTwitter import ApoyoTwitter
from getAuthorizations import GetAuthorizations

class RecolectorTweetsLangStream(TwythonStreamer, Recolector):
	"""docstring for TweetsStatusStream"""
	def __init__(self, escritores):
		self.authorizator = GetAuthorizations(1000)
		self.tipo_id = 100
		self.authorizator.load_twitter_token(self.tipo_id)
		app_key, app_secret, oauth_token, oauth_token_secret = self.authorizator.get_twitter_secret()

		Recolector.__init__(self, escritores)
		TwythonStreamer.__init__(self, app_key, app_secret, oauth_token, oauth_token_secret)

		self.tweets = []

	def recolecta(self, lang):
		self.statuses.filter(locations="-27,37,2,38",language=lang)
		#,language=lang

	def on_success(self, data):
		limiteEscritura = 20

		if 'text' in data:
			print len(self.tweets)
			if len(self.tweets) > limiteEscritura:
				print len(self.tweets)
				self.guarda(self.tweets)
				self.tweets = []
			self.tweets.append(data)


	def guarda(self, arrayDatos):
		for escritor in self.escritores:
			escritor.escribe(arrayDatos)

	def on_error(self, status_code, data):
		print "error"
		print status_code
		#exit()



if __name__ == '__main__':
	escritores = [EscritorTweetsCassandra(-1)]
	recolector = RecolectorTweetsLangStream(escritores)
	recolector.recolecta("es")