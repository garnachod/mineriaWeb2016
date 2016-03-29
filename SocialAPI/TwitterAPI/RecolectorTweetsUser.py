# -*- coding: utf-8 -*-
from SocialAPI.Recolector import Recolector
from ApoyoTwitter import ApoyoTwitter
from getAuthorizations import GetAuthorizations
from twython import Twython
from time import time

class RecolectorTweetsUser(Recolector):
	"""docstring for RecolectorTweetsUser"""
	def __init__(self, escritor):
		super(RecolectorTweetsUser, self).__init__(escritor)
		self.authorizator = GetAuthorizations(299)
		self.twitter = None
		self.apoyo = ApoyoTwitter()
		self.tipo_id = 1
		self.inicializa()
		#self.tiempos_por_escritor = {}
		

	def inicializa(self):
		self.authorizator.load_twitter_token(self.tipo_id)
		api_key, access_token = self.authorizator.get_twython_token()
		self.twitter = Twython(api_key, access_token=access_token)

	def recolecta(self, query=None, identificador=-1, limit=3200):
		arrayFinal = []

		if query is None and identificador == -1:
			raise Exception('Al menos debe haber un parametro usable')

		if query is not None:
			if query[0] == '@':
				query = query[1:]

		minimo = self.apoyo.getLastTweetCollected(screen_name=query, identificador=identificador)
		maximo = 0
		maximoGlobal = long(0)

		cont = 0
		flag_fin = False
		while True:
			try:
				statuses = self.privateRealizaConsulta(query=query, identificador=identificador, maxi=maximo, mini=minimo)
			except Exception, e:
				flag_fin = True
				statuses = []
			
			if len(statuses) == 0:
				break

			for status in statuses:
				arrayFinal.append(status)

			maximo = self.getMinIDtweets(arrayFinal, query)
			maximo -= 1
			if len(arrayFinal) > 50:
				self.guarda(arrayFinal)

				auxMax = self.getMaxIDtweets(arrayFinal, query)
				if auxMax > maximoGlobal:
					maximoGlobal = auxMax
					
				cont += len(arrayFinal)
				arrayFinal = []
			

			#limite de la api
			if len(arrayFinal) >= limit:
				break

		#fin del while
		self.guarda(arrayFinal)
		#for tipo in self.tiempos_por_escritor:
		#	print tipo + "\t" + str(self.tiempos_por_escritor[tipo])
		
		if maximoGlobal != 0:
			self.apoyo.setLastUserTweet(maximoGlobal, screen_name=query, identificador=identificador)


		if flag_fin == True:
			raise Exception('LIMITE')

	def guarda(self, arrayDatos):
		for escritor in self.escritores:
			#medicion de tiempos
			#tipo_escritor = escritor.__class__.__name__
			#if tipo_escritor not in self.tiempos_por_escritor:
			#	self.tiempos_por_escritor[tipo_escritor] = 0
			#tiempo_inicio = time()
			escritor.escribe(arrayDatos)
			#self.tiempos_por_escritor[tipo_escritor] += time() - tiempo_inicio
		

	def getMinIDtweets(self, tweets, query):

		minimo = long(10**20)
		for tweet in tweets:
			if minimo > tweet["id"]:
				minimo = tweet["id"]
		if minimo == long(10**20):
			return 0

		return minimo

	def getMaxIDtweets(self, tweets, query):

		maximo = long(0)
		for tweet in tweets:
				if tweet["id"] > maximo:
					maximo = tweet["id"]

		return maximo


	def privateRealizaConsulta(self, query=None, identificador=-1, maxi=0, mini=0):
		#TODO busquedas por identificador
		if self.authorizator.is_limit_api(self.tipo_id):
			raise Exception('LIMITE')

		count = '200'
		try:
			if maxi == 0 and mini == 0: 
				if query is not None:
					retorno = self.twitter.get_user_timeline(screen_name=query, count=count)
				else:
					retorno = self.twitter.get_user_timeline(user_id=identificador, count=count)

			elif maxi == 0 and mini > 0:
				if query is not None:
					retorno = self.twitter.get_user_timeline(screen_name=query, since_id=mini, count=count)
				else:
					retorno = self.twitter.get_user_timeline(user_id=identificador, since_id=mini, count=count)

			elif maxi > 0 and mini == 0:
				if query is not None:
					retorno = self.twitter.get_user_timeline(screen_name=query, max_id=maxi, count=count)
				else:
					retorno = self.twitter.get_user_timeline(user_id=identificador, max_id=maxi, count=count)

			else:
				if mini > maxi:
					return []
					
				if query is not None:
					retorno = self.twitter.get_user_timeline(screen_name=query, max_id=maxi, since_id=mini, count=count)
				else:
					retorno = self.twitter.get_user_timeline(user_id=identificador, max_id=maxi, since_id=mini, count=count)

			self.authorizator.add_query_to_key(self.tipo_id)
			return retorno
		except Exception, e:
			print e
			self.authorizator.add_query_to_key(self.tipo_id)
			if "429" in str(e):
				raise Exception('LIMITE')
			return []
			

	def privateParseaStatus(self, status):
		arrayTweets = []
		
		arrayTweets.append(status)

		return arrayTweets

	def privateParseaUserFormStatus(self, userAPI):
		user = {}
		#id
		user["id"] = userAPI["id"]
		#name
		user["name"] = userAPI["name"]
		#screen name
		user["screen_name"] = userAPI["screen_name"]
		#location
		user["location"] = userAPI["location"]
		#followers_count
		user["followers_count"] = userAPI["followers_count"]
		#created_at
		user["created_at"] = userAPI["created_at"]

		return user