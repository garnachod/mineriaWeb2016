from PostgreSQL.ConexionSQL import ConexionSQL 
from Cassandra.ConexionCassandra import ConexionCassandra
from ConsultasSQL import ConsultasSQL
from ConsultasCassandra import ConsultasCassandra
from collections import namedtuple

class ConsultasGeneral(ConsultasSQL, ConsultasCassandra): 
	"""docstring for ConsultasGeneral"""
	def __init__(self):
		super(ConsultasGeneral, self).__init__()

		conSql = ConexionSQL()
		self.conn = conSql.getConexion()
		self.cur = conSql.getCursor()

		self.cassandra_active = True

	def setAppSearchTime(self, searchID, time):
		query = "UPDATE app_searches SET search_time=%s WHERE id=%s;"
		try:
			self.cur.execute(query, [time, searchID])
			self.conn.commit()

			return True
		except Exception, e:
			print str(e)
			return False

	def getTareasPendientesTotal(self):
		query = "SELECT * from tareas_programadas where tiempo_fin > CURRENT_TIMESTAMP"
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def getTareasTerminadasTotal(self):
		query = "SELECT * from tareas_programadas where tiempo_fin < CURRENT_TIMESTAMP"
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False


	def getBusquedaFromIdBusqueda(self, idbusqueda):
		query = "SELECT search_string, id_user FROM app_searches where id = %s;"
		try:
			self.cur.execute(query, [idbusqueda, ])
			row = self.cur.fetchone()
		
			return row[0], row[1]
		except Exception, e:
			print str(e)
			return False, False


	def getTweetStatus(self, identificador):
		if self.cassandra_active:
			return self.getTweetStatusCassandra(identificador)
		else:
			return self.getTweetStatusSQL(identificador)

	def getScreenNameByUserID(self, identificador):
		if self.cassandra_active:
			return self.getScreenNameByUserIDCassandra(identificador)
		else:
			raise Exception('No implementado')



	def getIDTweetsTrainList(self, id_lista_entrenamiento):
		query = """SELECT id_tweet FROM tweets_entrenamiento as tw WHERE tw.clase != 'no_usar' AND tw.id_lista = %s;"""
		print id_lista_entrenamiento
		try:
			self.cur.execute(query, [id_lista_entrenamiento, ])
			rows = self.cur.fetchall()
			lista = []
			for row in rows:
				lista.append(row[0])

			return lista
		except Exception, e:
			print str(e)
			return False

	def getIDsANDClassEntrenamiento(self, identificador_lista):
		query = "SELECT id_tweet, clase FROM tweets_entrenamiento WHERE id_lista = %s AND clase != 'no_usar';"

		try:
			self.cur.execute(query, [identificador_lista, ])
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def getTweetsAndClassTrain(self, id_lista):
		if self.cassandra_active:
			Row = namedtuple('Row', 'status, clase')
			tweets = self.getIDsANDClassEntrenamiento(id_lista)
			retorno = []
			for tweet in tweets:
				status = self.getTweetStatusCassandra(tweet[0])
				row = Row(status, tweet[1])
				retorno.append(row)

			return retorno
		else:
			return self.getTweetsAndClassTrainSQL(id_lista)


	def creaListaEntrenamiento(self, nombre, id_usuario):
		query = """INSERT INTO listas_entrenamiento (nombre, id_username) VALUES (%s, %s)"""
		#query = "INSERT INTO tweets_entrenamiento (id_tweet,clase) VALUES (%s,%s);"
		try:
			self.cur.execute(query, [nombre, id_usuario])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en creaListaEntrenamiento"
			print str(e)
			return False

	def getListasEntrenamiento(self, id_usuario):
		query = "SELECT id, nombre FROM listas_entrenamiento WHERE id_username = %s;"
		try:
			self.cur.execute(query, [id_usuario, ])
			rows = self.cur.fetchall()

			return rows
		except Exception, e:
			print str(e)
			return False
	
	def deleteListaEntrenamiento(self, identificador):
		query = 'DELETE FROM listas_entrenamiento WHERE id=%s;'
		try:
			self.cur.execute(query, [identificador, ])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en deleteListaEntrenamiento"
			print str(e)
			return False

	def getTweetByIDLarge(self, identificador):
		if self.cassandra_active:
			return self.getTweetByIDLargeCassandra(identificador)
		else:
			return self.getTweetByIDLargeSQL(identificador)


	#TODO Controlar los tiempos segun crece la DB
	def getIDsTweetsTrain(self, topics, limit, lista_id):
		if self.cassandra_active:
			#busca los tweets y eliminar los ids que ya se hayan insertado
			tweets_ya_insertados = self.getIDsTweetsEnTrain(lista_id)
			#print len(tweets_ya_insertados)
			#aumenta el limite mirando los tweets en la lista
			limit = len(tweets_ya_insertados) + limit
			tweets_no_filtrados = self.getIDsTweetsTrainCassandra(topics, limit)
			tweets_filtrados = []
			for tweet_no_filtrados in tweets_no_filtrados:
				if tweet_no_filtrados[0] not in tweets_ya_insertados:
					tweets_filtrados.append(tweet_no_filtrados)

			return tweets_filtrados
		else:
			topics_sql = topics.replace(", ", ",").split(",")
			return self.getIDsTweetsTrainSQL(topics_sql, limit)


	def getIDsTweetsEnTrain(self, lista_id):
		"""Retorna un diccionario {} de IDs para que sea sencillo hacer un filtrado"""
		query = "SELECT id_tweet FROM tweets_entrenamiento WHERE id_lista = %s;"

		try:
			self.cur.execute(query, [lista_id, ])
			rows = self.cur.fetchall()
			retorno = {}
			for row in rows:
				retorno[row[0]] = 1

			return retorno
		except Exception, e:
			print "error en getIDsTweetsEnTrain"
			print str(e)
			return False

	def setTweetTrainID(self, identificador, clase, id_lista):
		query = """INSERT INTO tweets_entrenamiento (id_tweet, clase, id_lista)
					SELECT %s, %s, %s
					WHERE NOT EXISTS (SELECT id FROM tweets_entrenamiento WHERE id_tweet=%s AND id_lista=%s);"""

		#query = "INSERT INTO tweets_entrenamiento (id_tweet,clase) VALUES (%s,%s);"

		try:
			self.cur.execute(query, [identificador, clase, id_lista, identificador, id_lista])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en setTweetTrainID"
			print str(e)
			return False

	def getClaseTrainID(self, identificador):
		query = """SELECT clase FROM tweets_entrenamiento WHERE id_tweet = %s;"""

		try:
			self.cur.execute(query, [identificador, ])
			row = self.cur.fetchone()
			if row is None:
				return False

			return row
		except Exception, e:
			print "error en getClaseTrainID"
			print str(e)
			return False

	def changeClaseTweet(self, identificador, clase):
		query = """UPDATE tweets_entrenamiento SET clase = %s WHERE id_tweet = %s;"""

		try:
			self.cur.execute(query, [clase, identificador])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en changeClaseTweet"
			print str(e)
			return False

	def creaEntrenamientoRetID(self, tipo, id_lista_entrenamiento):
		query = """INSERT INTO entrenamientos (tipo, id_lista_entrenamiento) VALUES (%s, %s) RETURNING id;"""
		try:
			self.cur.execute(query, [tipo, id_lista_entrenamiento])
			Id = self.cur.fetchone()[0]
			self.conn.commit()

			return Id
			
		except Exception, e:
			print str(e)
			return -1

	def editEntrenamiento(self, identificador, ficheroARFF, ficheroJSON, error):
		query = """UPDATE entrenamientos SET fichero_arff = %s, fichero_json = %s, porcentaje_fallo = %s WHERE id = %s;"""

		try:
			self.cur.execute(query, [ficheroARFF, ficheroJSON, error, identificador])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en editEntrenamiento"
			print str(e)
			return False

	def getFilesLastTrainTweet(self, id_lista):
		query = "SELECT fichero_arff, fichero_json FROM entrenamientos WHERE tipo = 'tweet' and id_lista_entrenamiento = %s and fichero_arff != '' ORDER BY id DESC LIMIT 1;"
		try:
			self.cur.execute(query, [id_lista, ])
			row = self.cur.fetchone()

			return row
		except Exception, e:
			print "error en getFilesLastTrainTweet"
			print str(e)
			return False

	def getTweetsIdBusquedaNoAnalizada(self, searchID):
		query = "SELECT j.id_tweet FROM join_search_tweet as j WHERE j.id_search = %s AND j.id_tweet NOT IN (SELECT c.id_tweet from clasificaciontweets as c);"
		try:
			self.cur.execute(query, [searchID, ])
			rows = self.cur.fetchall()

			return rows
		except Exception, e:
			print "error en getTweetsIdBusquedaNoAnalizada"
			print str(e)
			return False

	def getTweetsIdBusquedaTodos(self, searchID):
		query = "SELECT j.id_tweet FROM join_search_tweet as j WHERE j.id_search = %s;"
		try:
			self.cur.execute(query, [searchID, ])
			rows = self.cur.fetchall()

			return rows
		except Exception, e:
			print "error en getTweetsIdBusquedaTodos"
			print str(e)
			return False

	def getSearchIDFromIDTarea(self, idTarea):
		query = """SELECT id_search FROM tareas_programadas WHERE id = %s;"""
		try:
			self.cur.execute(query, [idTarea, ])
			row = self.cur.fetchone()

			return row[0]
		except Exception, e:
			print "error en getSearchIDFromIDTarea"
			print str(e)
			return False

	def insertTweetAnalizado(self, id_tweet, clase):
		query = """INSERT INTO clasificaciontweets (id_tweet, clase) VALUES (%s, %s);"""
		try:
			self.cur.execute(query, [id_tweet, clase])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en insertTweetAnalizado"
			print str(e)
			return False

	def editTweetAnalizado(self, id_tweet, clase):
		query = """UPDATE clasificaciontweets set clase=%s WHERE id_tweet=%s;"""
		try:
			self.cur.execute(query, [clase, id_tweet])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en editTweetAnalizado"
			print str(e)
			return False

	def getIdListaEntrenamientoByIDSearch(self, id_search):
		query = """SELECT id_lista_entrenamiento FROM tareas_programadas WHERE id_search = %s;"""
		try:
			self.cur.execute(query, [id_search, ])
			row = self.cur.fetchone()

			return row[0]
		except Exception, e:
			print "error en getIdListaEntrenamientoByIDSearch"
			print str(e)
			return False

	def isListasEntrenamientoFromUser(self, id_user, id_lista):
		query = """SELECT * FROM listas_entrenamiento WHERE id_username = %s and id = %s;"""

		try:
			self.cur.execute(query, [id_user, id_lista])
			row = self.cur.fetchone()

			if row is None:
				return False
			else:
				return True

		except Exception, e:
			print "error en isListasEntrenamientoFromUser"
			print str(e)
			return False
		
	def getLastTweetCollectedScreenName(self, screen_name):
		if screen_name[0] == '@':
			screen_name = screen_name[1:]

		if self.cassandra_active:
			return self.getLastTweetCollectedScreenNameCassandra(screen_name)
		else:
			return self.getLastTweetCollectedScreenNameSQL(screen_name)

	def getLastTweetCollectedIdentificador(self, identificador):
		if self.cassandra_active:
			return self.getLastTweetCollectedIdentificadorCassandra(identificador)
		#else:
		#	return self.getLastTweetCollectedScreenNameSQL(screen_name)
		else:
			raise Exception('No implementado')

	def setLastTweetCollectedScreenName(self, screen_name, maximo):
		if screen_name[0] == '@':
			screen_name = screen_name[1:]

		if self.cassandra_active:
			return self.setLastTweetCollectedScreenNameCassandra(screen_name, maximo)
		else:
			return self.setLastTweetCollectedScreenNameSQL(screen_name, maximo)

	def setLastTweetCollectedIdentificador(self, identificador, maximo):
		if self.cassandra_active:
			return self.setLastTweetCollectedIdentificadorCassandra(identificador, maximo)
		#else:
		#	return self.setLastTweetCollectedScreenNameSQL(screen_name, maximo)
		else:
			raise Exception('No implementado')


	def getQueryFromSearchID(self, searchID):
		query = "SELECT search_string FROM app_searches where id = %s;"
		try:
			self.cur.execute(query, [searchID, ])
			row = self.cur.fetchone()

			return row[0]
		except Exception, e:
			print str(e)
			return False

	def getUserIDByScreenName(self, twitterUser):
		if twitterUser[0] == '@':
			twitterUser = twitterUser[1:]

		if self.cassandra_active:
			return self.getUserIDByScreenNameCassandra(twitterUser)
		else:
			return self.getUserIDByScreenNameSQL(twitterUser)