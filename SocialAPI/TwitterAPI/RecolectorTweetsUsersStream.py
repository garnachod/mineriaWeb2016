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

class RecolectorTweetsUsersStream(TwythonStreamer, Recolector):
	"""docstring for TweetsStatusStream"""
	def __init__(self, escritores):
		self.authorizator = GetAuthorizations(1000)
		self.tipo_id = 100
		self.authorizator.load_twitter_token(self.tipo_id)
		app_key, app_secret, oauth_token, oauth_token_secret = self.authorizator.get_twitter_secret()

		Recolector.__init__(self, escritores)
		TwythonStreamer.__init__(self, app_key, app_secret, oauth_token, oauth_token_secret)

		self.tweets = []

	def recolecta(self, tokens):
		string_tokens = ""
		for i, token in enumerate(tokens):
			if i >= 5000:
				break
			if i == 0:
				string_tokens += str(token)
			else:
				string_tokens += "," + str(token)

		print string_tokens

		self.statuses.filter(follow=string_tokens)

	def on_success(self, data):
		limiteEscritura = 10

		if 'text' in data:
			print len(self.tweets)
			if len(self.tweets) > limiteEscritura:
				self.guarda(self.tweets)
				self.tweets = []
			self.tweets.append(data)


	def guarda(self, arrayDatos):
		for escritor in self.escritores:
			escritor.escribe(arrayDatos)

	def on_error(self, status_code, data):
		print status_code
		#exit()



if __name__ == '__main__':
	escritores = [EscritorTweetsCassandra(-1)]
	recolector = RecolectorTweetsUsersStream(escritores)
	recolector.recolecta([2383366169])