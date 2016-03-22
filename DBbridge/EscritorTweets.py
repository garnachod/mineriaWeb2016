from Escritor import Escritor
from PostgreSQL.ConexionSQL import ConexionSQL
import json
import datetime
class EscritorTweets(Escritor):
	"""docstring for EscritorTweets"""
	def __init__(self, searchID):
		super(EscritorTweets, self).__init__(searchID)
		conSql = ConexionSQL()
		self.conn = conSql.getConexion()
		self.cur = conSql.getCursor()
		self.hashCache = {}

	def escribe(self, data):
		for tweet in data:
			#escribe tweet DB
			id_api_twitter = tweet["user"]["id"]
			#se evitan muchos accesos a la db con este simple codigo
			hash_id = self.getUserByAPIUserIDHash(id_api_twitter)
			if hash_id != -1:
				self.escribeTweet(tweet, hash_id)
			else:
				db_id = self.getUserByAPIUserID(id_api_twitter)
				if db_id != -1: 
					#self.actualizaUsuario(tweet["user"])
					self.escribeTweet(tweet, db_id)
				else:
					db_id = self.insertaUsuario(tweet["user"])
					self.escribeTweet(tweet, db_id)

				self.putUserByAPIUserIDHash(id_api_twitter, db_id)

	def escribeTweet(self, tweet, userid):
		id_api_twitter = tweet["id"]
		db_id = self.getTweetSiExisteAPIID(id_api_twitter)
		if db_id != -1:
			#self.actualizaTweet(tweet)
			pass
		else:
			db_id = self.insertaTweet(tweet)
			#self.insertaJoinTable(self.searchID, db_id)

		

	'''
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
	'''

	def getTweetSiExisteAPIID(self, apiID):

		query = "SELECT id_twitter FROM tweets WHERE id_twitter = %s;"
		try:
			self.cur.execute(query, [apiID, ])
			row = self.cur.fetchone()
			if row is None:
				return -1

			return row[0]
		except Exception, e:
			print str(e)
			return -1
		

	def insertaTweet(self, data):
		created_at = datetime.datetime.strptime(data["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
		identificador = data["id"]
		text = data["text"]
		lang = data["lang"]
		user_id = data["user"]["id"]
		#Controla si existen RTs dentro del Tweet
		retweet_count = 0
		if "retweet_count" in data:
			retweet_count = data["retweet_count"]
		#Controla si existen FAVs dentro del Tweet
		favorite_count = 0
		if "favorite_count" in data:
			favorite_count = data["favorite_count"]
		
		#Controla si es RT para almacenar la informacion
		is_rt = False
		rt_id = 0
		if "retweeted_status" in data:
			is_rt = True
			rt_id = data["retweeted_status"]["id"]

		media = ""


		query = """INSERT INTO tweets (id_twitter, status, tuser, created_at, lang, is_retweet, orig_tweet, favorite_count, retweet_count, media_url) 
				   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_twitter;"""
		#query = "INSERT INTO tweets_entrenamiento (id_tweet,clase) VALUES (%s,%s);"
		try:

			self.cur.execute(query, [identificador, text[:160], user_id, created_at,lang[:3], is_rt, rt_id,favorite_count,retweet_count,media])
			Id = self.cur.fetchone()[0]
			self.conn.commit()

			return Id
		except Exception, e:
			print "error en insertaTweet Twitter"
			print str(e)
			return -1

	def actualizaTweet(self, tweet):
		query = """UPDATE tweets SET favorite_count=%s, retweet_count=%s WHERE id_twitter=%s;"""
		try:
			self.cur.execute(query, [tweet["favorite_count"],tweet["retweet_count"],tweet["id"]])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en actualizaTweet Twitter"
			print str(e)
			return False

	def getUserByAPIUserIDHash(self, apiUserID):
		return -1
		"""if apiUserID in self.hashCache:
			return self.hashCache[apiUserID]

		return -1
		"""

	def putUserByAPIUserIDHash(self, apiUserID, identificador):
		self.hashCache[apiUserID] = identificador

	def getUserByAPIUserID(self, apiUserID):
		#select returning id
		query = "SELECT id_twitter FROM users WHERE id_twitter = %s;"
		try:
			self.cur.execute(query, [apiUserID, ])
			row = self.cur.fetchone()
			if row is None:
				return -1

			return row[0]
		except Exception, e:
			print str(e)
			return -1
		

	def insertaUsuario(self, data):
		identificador = data["id"]
		#name
		name = data["name"]
		#screen name
		screen_name = data["screen_name"]
		#location
		location = data["location"]
		#followers_count
		followers_count = data["followers_count"]
		#created_at
		created_at = datetime.datetime.strptime(data["created_at"], '%a %b %d %H:%M:%S +0000 %Y')

		query = """INSERT INTO users (id_twitter, name, screen_name, followers, location, created_at) 
				   VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_twitter;"""
		#query = "INSERT INTO tweets_entrenamiento (id_tweet,clase) VALUES (%s,%s);"
		try:
			self.cur.execute(query, [identificador, name[:20], screen_name[:15], followers_count, location[:50], created_at])
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
		