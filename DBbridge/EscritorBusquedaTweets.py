from Escritor import Escritor
from PostgreSQL.ConexionSQL import ConexionSQL
import threading

class EscritorBusquedaTweets(Escritor):
	"""docstring for EscritorTweets"""
	def __init__(self, searchID):
		super(EscritorBusquedaTweets, self).__init__(searchID)
		conSql = ConexionSQL()
		self.conn = conSql.getConexion()
		self.cur = conSql.getCursor()
		self.active_asinc = True

	def escribe(self, data):
		if self.active_asinc:
			array_ids = []
			for tweet in data:
				array_ids.append(tweet["id"])

			escritor = _EscritorBusquedaTweetsAsinc(array_ids, self.searchID)
			escritor.start()
		else:
			for tweet in data:
				id_api_twitter = tweet["id"]
				self.insertaJoinTable(self.searchID, id_api_twitter)

	def insertaJoinTable(self, id_search, id_tweet):
		query = """INSERT INTO join_search_tweet (id_search, id_tweet) SELECT %s, %s
					WHERE NOT EXISTS (SELECT * FROM join_search_tweet WHERE id_search=%s AND id_tweet=%s);"""
		try:
			self.cur.execute(query, [id_search, id_tweet, id_search, id_tweet])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en insertaJoinTable Twitter"
			print str(e)
			return False

class _EscritorBusquedaTweetsAsinc(threading.Thread):
	def __init__(self, array_ids, id_busqueda):
		threading.Thread.__init__(self)
		conSql = ConexionSQL()
		self.conn = conSql.getConexion()
		self.cur = conSql.getCursor()
		self.array_ids = list(array_ids)
		self.id_busqueda = id_busqueda

	def run(self):
		for identificador in self.array_ids:
			self.insertaJoinTable(self.id_busqueda, identificador)

	def insertaJoinTable(self, id_search, id_tweet):
		query = """INSERT INTO join_search_tweet (id_search, id_tweet) SELECT %s, %s
					WHERE NOT EXISTS (SELECT * FROM join_search_tweet WHERE id_search=%s AND id_tweet=%s);"""
		try:
			self.cur.execute(query, [id_search, id_tweet, id_search, id_tweet])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en insertaJoinTable Twitter"
			print str(e)
			return False