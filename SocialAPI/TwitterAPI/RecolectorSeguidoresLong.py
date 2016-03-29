# -*- coding: utf-8 -*-
from SocialAPI.Recolector import Recolector
from ApoyoTwitter import ApoyoTwitter
from getAuthorizations import GetAuthorizations
from twython import Twython

class RecolectorSeguidoresLong(Recolector):
	"""docstring for RecolectorSeguidores"""
	def __init__(self, escritor):
		super(RecolectorSeguidoresLong, self).__init__(escritor)
		self.authorizator = GetAuthorizations(30)
		self.twitter = None
		self.apoyo = ApoyoTwitter()
		self.tipo_id = 3
		self.inicializa()
		self.cursor = -1
		

	def inicializa(self):
		self.authorizator.load_twitter_token(self.tipo_id)
		api_key, access_token = self.authorizator.get_twython_token()
		self.twitter = Twython(api_key, access_token=access_token)

	def recolecta(self, query):
		self.cursor = -1
		arrayUsuarios = []

		if query[0] == '@':
			query = query[1:]

		while True:
			retorno = self.privateRealizaConsulta(query)
			if retorno == []:
				break

			self.cursor = retorno["next_cursor"]

			for usuario_np in retorno["users"]:
				usuario_p = self.privateParseaUserFormStatus(usuario_np)
				arrayUsuarios.append(usuario_p)

		self.guarda(arrayUsuarios)

	def guarda(self, arrayDatos):
		self.escritor.escribe(arrayDatos)

	def privateRealizaConsulta(self, query):
		if self.authorizator.is_limit_api(self.tipo_id):
				return []

		try:
			retorno = self.twitter.get_followers_list(screen_name=query, cursor=self.cursor, count='200')
			self.authorizator.add_query_to_key(self.tipo_id)

			if retorno["users"] == []:
				return []

			return retorno
		except Exception, e:
			print e
			return []

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
