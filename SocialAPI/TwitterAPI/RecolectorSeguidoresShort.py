from SocialAPI.Recolector import Recolector
from ApoyoTwitter import ApoyoTwitter
from getAuthorizations import GetAuthorizations
from twython import Twython
 
class RecolectorSeguidoresShort(Recolector):
	def __init__(self, escritores):
		super(RecolectorSeguidoresShort, self).__init__(escritores)
		self.authorizator = GetAuthorizations(15)
		self.twitter = None
		self.apoyo = ApoyoTwitter()
		self.tipo_id = 4
		self.inicializa()
		self.cursor = -1
		self.lastQuery = ""
		

	def inicializa(self):
		self.authorizator.load_twitter_token(self.tipo_id)
		api_key, access_token = self.authorizator.get_twython_token()
		self.twitter = Twython(api_key, access_token=access_token)

	def cleanCursor(self):
		self.cursor = -1

	def recolecta(self, query=None, id_user = -1, complete=False):

		if query is None and id_user == -1:
			raise Exception('Al menos debe haber un parametro usable')

		if query is not None:
			if query[0] == '@':
				query = query[1:]

			if self.lastQuery == query:
				print "query es igual"
				return
			else:
				self.lastQuery = query
				self.cursor = -1

			id_user = self.apoyo.getUserIDByScreenName(query)
			if id_user == None:
				raise Exception('El usuario debe estar en la base de datos')
		else:
			self.cursor = -1
			
		
		retornoFinal = {"ids": []}
		while True:
			retorno = self.privateRealizaConsultaById(id_user)
			print self.cursor
			if retorno == []:
				break

			retornoFinal["ids"].extend(retorno["ids"])

			if len(retorno["ids"]) < 5000:
				break

			if complete == False:
				break

		
		#se almacenan las relaciones en una tupla (usuario1, usuario2)
		#esto quiere decir que el usuario1 sigue al usuario2.
		lista_relaciones = []
		for identificador in retornoFinal["ids"]:
			lista_relaciones.append((identificador, id_user))

		self.guarda(lista_relaciones)

	def guarda(self, arrayDatos):
		for escritor in self.escritores:
			escritor.escribe(arrayDatos)
			

	def privateRealizaConsultaById(self, identificador):
		if self.authorizator.is_limit_api(self.tipo_id):
			raise Exception('LIMITE')

		try:
			retorno = self.twitter.get_followers_ids(user_id=identificador, cursor=self.cursor, count='5000')
			self.authorizator.add_query_to_key(self.tipo_id)
			if len(retorno["ids"]) == 0:
				return []

			self.cursor = retorno["next_cursor"]

			return retorno
		except Exception, e:
			self.authorizator.add_query_to_key(self.tipo_id)
			if "429" in str(e):
				raise Exception('LIMITE')

			print e
			return []

