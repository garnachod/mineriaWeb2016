from PostgreSQL.ConexionSQL import ConexionSQL 

class ConsultasSQL(object):
	"""docstring for ConsultasSQL"""
	def __init__(self):
		super(ConsultasSQL, self).__init__()
		conSql = ConexionSQL()
		self.conn_sql = conSql.getConexion()
		self.cur_sql = conSql.getCursor()


	def getTweetsUsuarioSQL(self, twitterUser, use_max_id=False, max_id=0, limit=1000):
		if use_max_id == True:
			query = "SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name FROM tweets as t, users as u WHERE u.screen_name = %s and u.id_twitter = t.tuser order by t.created_at DESC LIMIT %s;"
			try:
				self.cur_sql.execute(query, [twitterUser, ])
				row = self.cur_sql.fetchall()
				
				return row
			except Exception, e:
				print str(e)
				return False
		else:
			query = "SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name FROM tweets as t, users as u WHERE u.screen_name = %s and u.id_twitter = t.tuser order by t.created_at DESC LIMIT %s;"
			try:
				self.cur_sql.execute(query, [twitterUser, limit])
				row = self.cur_sql.fetchall()
				
				return row
			except Exception, e:
				print str(e)
				return False
		
	def getUserIDByScreenNameSQL(self, twitterUser):
		query = "SELECT id_twitter FROM users WHERE screen_name = %s LIMIT 1;"

		try:
			self.cur_sql.execute(query, [twitterUser,])
			row = self.cur_sql.fetchone()
			
			return row[0]
		except Exception, e:
			print str(e)
			return 0

	def getLastTweetCollectedScreenNameSQL(self, screen_name):
		query = "SELECT last_tweet_collected FROM users WHERE screen_name=%s;"
		try:
			print screen_name
			self.cur.execute(query, [screen_name, ])
			row = self.cur.fetchone()
			if row is None:
				return 0
			if row[0] is None:
				return 0

			#print long(row[0])
			return long(row[0])
		
		except Exception, e:
			print str(e)
			return 0

	def setLastTweetCollectedScreenNameSQL(self, screen_name, maximo):
		query = "UPDATE users SET last_tweet_collected=%s WHERE screen_name=%s;"
		try:
			self.cur.execute(query, [maximo, screen_name])
			self.conn.commit()

			return True
		except Exception, e:
			print str(e)
			return False

	def getTweetStatusSQL(self, identificador):
		query = "SELECT status FROM tweets WHERE id_twitter = %s;"
		try:
			self.cur.execute(query, [identificador, ])
			row = self.cur.fetchone()

			return row[0]
		except Exception, e:
			print str(e)
			return False


	def getTweetByIDLargeSQL(self, identificador):
		query = """SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name 
				   FROM tweets as t, users as u 
				   WHERE t.id_twitter = %s and t.tuser = u.id_twitter LIMIT 1;"""
		try:
			self.cur.execute(query, [identificador, ])
			row = self.cur.fetchone()

			return row
		except Exception, e:
			print str(e)
			return False


	def getTweetsTopicsSQL(self, topics):
		#SELECT * from tweets WHERE status LIKE '%beta%' or status LIKE '%@garnachod%'

		query = "SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name "
		query += "FROM tweets as t, users as u "
		query += "WHERE ("
		i = 0
		for topic in topics:
			if " " in topic:
				subtopics = topic.split(" ")
				topics[i] = '%'
				for subtopic in subtopics:
					topics[i] += subtopic + '%'
			else:
				topics[i] = '%' + topic + '%'

			if i == 0:
				query += " status LIKE %s"
			else:
				query += " or status LIKE %s"
			i = i + 1

		query += "  ) and is_retweet is False and (lang = 'es' or lang = 'en') and t.tuser = u.id_twitter order by t.created_at DESC LIMIT 2000;"
		print query
		print topics
		try:
			self.cur.execute(query, topics)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False


	def getIDsTweetsTrainSQL(self, topics, limit):
		query = "SELECT t.id_twitter "
		query += "FROM tweets as t "
		query += "WHERE ("
		i = 0
		for topic in topics:
			if " " in topic:
				subtopics = topic.split(" ")
				topics[i] = '%'
				for subtopic in subtopics:
					topics[i] += subtopic + '%'
			else:
				topics[i] = '%' + topic + '%'


			if i == 0:
				query += " status LIKE %s"
			else:
				query += " or status LIKE %s"
			i = i + 1

		query += "  ) and is_retweet = False and id_twitter not in (SELECT id_tweet FROM tweets_entrenamiento) and (lang = 'es' or lang = 'en') order by t.created_at DESC LIMIT %s;"

		parameters = list(topics)
		parameters.append(limit)
		try:
			self.cur.execute(query, parameters)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def getNumTweetsNoRTSQL(self):
		query ="SELECT count(id_twitter) FROM tweets WHERE is_retweet = FALSE;"
		try:
			self.cur.execute(query)
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getNumTweetsSiRT(self):
		query ="SELECT count(id_twitter) FROM tweets WHERE is_retweet = TRUE;"
		try:
			self.cur.execute(query)
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getNumTweetsNoMediaSQL(self):
		query ="SELECT count(id_twitter) FROM tweets WHERE media_url is NULL and is_retweet = FALSE;"
		try:
			self.cur.execute(query)
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getNumTweetsSiMediaSQL(self):
		query ="SELECT count(id_twitter) FROM tweets WHERE media_url is NOT NULL and is_retweet = FALSE;"
		try:
			self.cur.execute(query)
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getTweetsEntrenamientoListarSQL(self, identificador):
		query = """SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name, t.id_twitter, te.clase 
				FROM tweets as t, users as u, tweets_entrenamiento as te , listas_entrenamiento as li
				WHERE te.clase != 'no_usar' and li.id = id_lista and li.id = %s and te.id_tweet = t.id_twitter and u.id_twitter = t.tuser order by te.id DESC;
				"""
		
		try:
			self.cur.execute(query, [identificador, ])
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def getTweetsAndClassTrainSQL(self, id_lista):
		query = "SELECT status, clase FROM tweets as t, tweets_entrenamiento as tw WHERE t.id_twitter = tw.id_tweet and tw.id_lista = %s and tw.clase != 'no_usar'"
		try:
			self.cur.execute(query, [id_lista, ])
			rows = self.cur.fetchall()

			return rows
		except Exception, e:
			print str(e)
			return False