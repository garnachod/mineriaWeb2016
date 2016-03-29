from Escritor import Escritor
from PostgreSQL.ConexionSQL import ConexionSQL

class EscritorSeguidoresSQL(Escritor):
	"""docstring for EscritorSeguidores"""
	def __init__(self, searchID):
		super(EscritorSeguidores, self).__init__(searchID)
		conSql = ConexionSQL()
		self.conn = conSql.getConexion()
		self.cur = conSql.getCursor()

	def escribe(self, data):

		query = self.getQueryFromSearchID(self.searchID)
		if query == False:
			return

		if query[0] == "@":
			query = query[1:]

		user_id = self.getUserByScreenNameUserID(query)
		
		if user_id == -1:
			return

		for user in data:
			db_id = self.getUserByAPIUserID(user["id"])
			if db_id != -1:
				self.actualizaUsuario(user)
			else:
				db_id = self.insertaUsuario(user)

			self.insertaJoinTable(user_id, db_id)

	def getQueryFromSearchID(self, searchID):
		query = "SELECT search_string FROM app_searches where id = %s;"
		try:
			self.cur.execute(query, [searchID, ])
			row = self.cur.fetchone()

			return row[0]
		except Exception, e:
			print str(e)
			return False


	def insertaJoinTable(self, id_user, id_follower):
		query = """INSERT INTO seguidores (id_user, id_seguidor) SELECT %s, %s
					WHERE NOT EXISTS (SELECT * FROM seguidores WHERE id_user=%s AND id_seguidor=%s);"""
		try:
			self.cur.execute(query, [id_user, id_follower, id_user, id_follower])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en insertaJoinTable Twitter"
			print str(e)
			return False

	def getUserByAPIUserID(self, apiUserID):
		#select returning id
		query = "SELECT id FROM users WHERE id_twitter = %s;"
		try:
			self.cur.execute(query, [apiUserID, ])
			row = self.cur.fetchone()
			if row is None:
				return -1

			return row[0]
		except Exception, e:
			print str(e)
			return -1

	def getUserByScreenNameUserID(self, screen_name):
		#select returning id
		query = "SELECT id FROM users WHERE screen_name = %s;"
		try:
			self.cur.execute(query, [screen_name, ])
			row = self.cur.fetchone()
			if row is None:
				return -1

			return row[0]
		except Exception, e:
			print str(e)
			return -1


	def insertaUsuario(self, usuario):
		query = """INSERT INTO users (id_twitter, name, screen_name, followers, location, created_at) 
				   VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"""
		#query = "INSERT INTO tweets_entrenamiento (id_tweet,clase) VALUES (%s,%s);"
		try:
			self.cur.execute(query, [usuario["id"], usuario["name"][:20], usuario["screen_name"][:15], usuario["followers_count"], usuario["location"][:50], usuario["created_at"]])
			Id = self.cur.fetchone()[0]
			self.conn.commit()

			return Id
		except Exception, e:
			print "error en insertaUsuario Twitter"
			print str(e)
			return -1


	def actualizaUsuario(self, usuario):
		#update
		query = """UPDATE users SET name=%s, followers=%s, location=%s WHERE id_twitter=%s;"""
		try:
			self.cur.execute(query, [usuario["name"][:20], usuario["followers_count"], usuario["location"][:50], usuario["id"]])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en actualizaUsuario Twitter"
			print str(e)
			return False
		