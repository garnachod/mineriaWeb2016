# -*- coding: utf-8 -*-
from SocialAPI.Recolector import Recolector
from ApoyoTwitter import ApoyoTwitter
from getAuthorizations import GetAuthorizations
from twython import Twython
from time import time

class RecolectorFavoritosUser(Recolector):
	def __init__(self, escritor):
		super(RecolectorFavoritosUser, self).__init__(escritor)
		self.authorizator = GetAuthorizations(14)
		self.twitter = None
		self.apoyo = ApoyoTwitter()
		self.tipo_id = 6
		self.inicializa()

	def inicializa(self):
		self.authorizator.load_twitter_token(self.tipo_id)
		api_key, access_token = self.authorizator.get_twython_token()
		self.twitter = Twython(api_key, access_token=access_token)

	def recolecta(self, query=None, id_user=-1, complete=False):
		#TODO recolectar todos los favoritos si flag activa
		if query is None and id_user == -1:
			raise Exception('Al menos debe haber un parametro usable')

		if query is not None:
			if query[0] == '@':
				query = query[1:]

			id_user = self.apoyo.getUserIDByScreenName(query)
			if id_user == None:
				raise Exception('El usuario debe estar en la base de datos')

		#print id_user
		maximo = 0
		while True:
			tweets = self.privateRealizaConsulta(id_user, maximo=maximo)
			if tweets == []:
				break

			relaciones = []
			for tweet in tweets:
				#el usuario1 -[:FAV]-> el tweet X
				relaciones.append((id_user, tweet["id"]))

			self.guarda(tweets, relaciones)

			if complete == False:
				break

			maximo = self.getMinIDtweets(tweets)
			maximo -= 1

			print maximo
	

	def guarda(self, arrayDatos, relaciones):
		#mal diseño sorry
		for escritor in self.escritores:
			if "EscritorTweets" in escritor.__class__.__name__:
				escritor.escribe(arrayDatos)
			else:
				escritor.escribe(relaciones)

	def getMinIDtweets(self, tweets):
		minimo = long(10**20)
		for tweet in tweets:
			if minimo > tweet["id"]:
				minimo = tweet["id"]
		if minimo == long(10**20):
			return 0

		return minimo

	def privateRealizaConsulta(self, identificador, maximo=0):
		count = 200
		if self.authorizator.is_limit_api(self.tipo_id):
			raise Exception('LIMITE')

		try:
			if maximo == 0:
				retorno = self.twitter.get_favorites(user_id=identificador, count=count)
			else:
				retorno = self.twitter.get_favorites(user_id=identificador, count=count, max_id=maximo)
			self.authorizator.add_query_to_key(self.tipo_id)

			return retorno
		except Exception, e:
			print e
			self.authorizator.add_query_to_key(self.tipo_id)
			if "429" in str(e):
				raise Exception('LIMITE')

			return []


