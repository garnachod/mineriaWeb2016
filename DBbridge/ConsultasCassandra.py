# -*- coding: utf-8 -*-

from Cassandra.ConexionCassandra import ConexionCassandra
from collections import namedtuple
from blist import blist
from ConsultasCassandraSpark import ConsultasCassandraSpark
import codecs
import time

class ConsultasCassandra(object):
	"""docstring for ConsultasCassandra"""
	def __init__(self):
		super(ConsultasCassandra, self).__init__()
		self.session_cassandra = ConexionCassandra().getSession()
		self.cassandra_spark = ConsultasCassandraSpark()
		#contiene identificador y valor
		self.memoria_temporal = {}
		
	def getTweetsUsuarioCassandra(self, twitterUser, use_max_id=False, max_id=0, limit=1000):
		"""
		Tweets de un usuario, informacion completa para la interfaz web y demas
		status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter, created_at, lang

		Parameters
		----------
		twitterUser : puede ser un identificador o un string del estilo "@usuario" con o sin @
		use_max_id : es por si se quiere hacer un filtro de tweets con id menor que el dado, si no se usa Cassandra tarda menos
		max_id : solo se usará si use_max_id es True
		limit : por defecto 1000 tweets, límite de tweets a retornar

		Returns
		-------
		iterator de Row(status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter, created_at, lang)
		"""

		user_id = None
		try:
			user_id = long(twitterUser)
		except Exception, e:
			if twitterUser[0] == "@":
				twitterUser = twitterUser[1:]
			user_id = self.getUserIDByScreenNameCassandra(twitterUser)

		if user_id is None:
			return []

		user = self.getUserByIDShortCassandra(user_id)
		if user == None:
			return []

		Row = namedtuple('Row', 'status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter, created_at, lang')
		if use_max_id:
			query = """SELECT status, favorite_count, retweet_count, orig_tweet, media_urls, id_twitter, created_at, lang  FROM tweets WHERE tuser = %s AND id_twitter < %s ORDER BY id_twitter DESC LIMIT %s;"""

			try:
				retorno = blist([])
				rows = self.session_cassandra.execute(query, [user_id, max_id, limit])
				for row in rows:
					nuevaFila = Row(row.status, row.favorite_count, row.retweet_count, row.orig_tweet, row.media_urls, user.screen_name, user.profile_img, row.id_twitter, row.created_at, row.lang)
					retorno.append(nuevaFila)
				return retorno
			except Exception, e:
				print "getTweetsUsuarioCassandra TRUE use_max_id"
				print e
				return []
		else:
			query = """SELECT status, favorite_count, retweet_count, orig_tweet, media_urls, id_twitter, created_at, lang FROM tweets WHERE tuser = %s ORDER BY id_twitter DESC LIMIT %s;"""

			try:
				retorno = blist([])
				rows = self.session_cassandra.execute(query, [user_id, limit])
				for row in rows:
					nuevaFila = Row(row.status, row.favorite_count, row.retweet_count, row.orig_tweet, row.media_urls, user.screen_name, user.profile_img, row.id_twitter, row.created_at, row.lang)
					retorno.append(nuevaFila)
				return retorno
			except Exception, e:
				print "getTweetsUsuarioCassandra FALSE use_max_id"
				print e
				return []

	def getTweetsUsuarioCassandra_lang(self, twitterUser, limit=200):
		"""
		Tweets de un usuario, solo la informacion del lenguaje

		Parameters
		----------
		twitterUser : usuario de twitter identificador o nombre
		limit : limite de tweets a devolver
		
		Returns
		-------
		iterator de Row(lang)
		"""
		user_id = None
		try:
			user_id = long(twitterUser)
		except Exception, e:
			if twitterUser[0] == "@":
				twitterUser = twitterUser[1:]
			user_id = self.getUserIDByScreenNameCassandra(twitterUser)

		if user_id is None:
			return []

		query = """SELECT lang FROM tweets WHERE tuser = %s ORDER BY id_twitter DESC LIMIT %s;"""
		try:
			return self.session_cassandra.execute(query, [user_id, limit])
		except Exception, e:
			print "getTweetsUsuarioCassandra_lang"
			print e
			return []

	def getTweetsUsuarioCassandra_statusAndLang(self, twitterUser, limit=3200):
		"""
		Tweets de un usuario, solo la informacion del texto y el lenguaje

		Parameters
		----------
		twitterUser : usuario de twitter identificador o nombre
		limit : limite de tweets a devolver
		
		Returns
		-------
		iterator de Row(status, lang)
		"""
		user_id = None
		try:
			user_id = long(twitterUser)
		except Exception, e:
			if twitterUser[0] == "@":
				twitterUser = twitterUser[1:]
			user_id = self.getUserIDByScreenNameCassandra(twitterUser)

		if user_id is None:
			return []

		query = """SELECT status, lang FROM tweets WHERE tuser = %s ORDER BY id_twitter DESC LIMIT %s;"""
		try:
			return self.session_cassandra.execute(query, [user_id, limit])
		except Exception, e:
			print "getTweetsUsuarioCassandra_lang"
			print e
			return []
		
	def getTweetsUsuarioCassandra_statusAndLang_noRT(self, twitterUser, limit=3200):
		"""
		Tweets de un usuario, solo la informacion del texto y el lenguaje

		Parameters
		----------
		twitterUser : usuario de twitter identificador o nombre
		limit : limite de tweets a devolver
		
		Returns
		-------
		iterator de Row(status, lang)
		"""
		user_id = None
		try:
			user_id = long(twitterUser)
		except Exception, e:
			if twitterUser[0] == "@":
				twitterUser = twitterUser[1:]
			user_id = self.getUserIDByScreenNameCassandra(twitterUser)

		if user_id is None:
			return []

		query = """SELECT status, lang, id_twitter FROM tweets WHERE tuser = %s AND orig_tweet = 0 LIMIT %s;"""

		try:
			tweets = []
			for tweet in self.session_cassandra.execute(query, [user_id, limit]):
				tweets.append(tweet)
			sortedTweets = sorted(tweets,key=lambda tweet: tweet.id_twitter, reverse=True)
			return sortedTweets
		except Exception, e:
			print "getTweetsUsuarioCassandra_lang"
			print e
			return []

	def getUserIDByScreenNameCassandra(self, twitterUser):
		"""
			Retorna el user_id asociado a un "usuario"
			si no existe el usuario, retorna False
		"""
		query = """SELECT id_twitter FROM users WHERE screen_name = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [twitterUser.lower()])
			if len(rows) == 0:
				return None

			return long(rows[0].id_twitter)
		except Exception, e:
			print "getUserIDByScreenNameCassandra"
			print e
			return None

	def getScreenNameByUserIDCassandra(self, user_id):
		"""
			dado un identificador, retona el screen_name de twitter,
			Retona False si no se ha encontrado
		"""
		query = """SELECT screen_name FROM users WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [user_id])
			if len(rows) == 0:
				return None

			return rows[0].screen_name
		except Exception, e:
			print "getUserIDByScreenNameCassandra"
			print e
			return None

	def getLastTweetCollectedScreenNameCassandra(self, twitterUser):
		"""
			last_tweet_collected es una variable que se guarda para optimizar y mucho la descarga de usuarios 
			simplemente hace un Get de la variable o 0 si nunca se ha descargado nada

			Get by screen_name

		"""
		query = """SELECT last_tweet_collected FROM users WHERE screen_name = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [twitterUser])
			if len(rows) == 0:
				return 0

			ltc = rows[0].last_tweet_collected
			if ltc is None:
				return 0

			return long(ltc)
		except Exception, e:
			print "getLastTweetCollectedScreenNameCassandra"
			print e
			return 0

	def getLastTweetCollectedIdentificadorCassandra(self, twitterUser):
		"""
			last_tweet_collected es una variable que se guarda para optimizar y mucho la descarga de usuarios 
			simplemente hace un Get de la variable o 0 si nunca se ha descargado nada

			Get by id_twitter

		"""
		query = """SELECT last_tweet_collected FROM users WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [twitterUser])
			if len(rows) == 0:
				return 0

			ltc = rows[0].last_tweet_collected
			if ltc is None:
				return 0

			return long(ltc)
		except Exception, e:
			print "getLastTweetCollectedScreenNameCassandra"
			print e
			return 0
	
	def setLastTweetCollectedScreenNameCassandra(self, twitterUser, maximo):
		"""
			last_tweet_collected es una variable que se guarda para optimizar y mucho la descarga de usuarios,
			simplemente hace un set de la variable

			SET desde un screen_name

			La logica final de este metodo depende de setLastTweetCollectedIdentificadorCassandra
		"""
		user_id = self.getUserIDByScreenNameCassandra(twitterUser)
		self.setLastTweetCollectedIdentificadorCassandra(user_id, maximo)

	def setLastTweetCollectedIdentificadorCassandra(self, twitterUser, maximo):
		"""
			last_tweet_collected es una variable que se guarda para optimizar y mucho la descarga de usuarios,
			simplemente hace un set de la variable

			SET desde un identificador de usuario
		"""
		query = "UPDATE users SET last_tweet_collected = %s WHERE id_twitter = %s;"
		try:
			self.session_cassandra.execute(query, (maximo, twitterUser))
			return True
		except Exception, e:
			print "setLastTweetCollectedScreenNameCassandra"
			print e
			return False

	def getOrigTweetAndCreatedAtFromTweetsByUser(self, twitterUser, limit=10000):
		"""
			retorna un Array de objetos, estos objetos solo contienen el orig_tweet y created_at
			permite que twitterUser sea del estilo "@usuario" o 123435345
			Recordemos: 
				created_at es un objeto dateTime
				orig_tweet es 0 si es un tweet del usuario, otro identificador si es un RT
		"""
		#Traduce el usuario a user_id
		user_id = None
		try:
			user_id = long(twitterUser)
		except Exception, e:
			if twitterUser[0] == "@":
				twitterUser = twitterUser[1:]
			user_id = self.getUserIDByScreenNameCassandra(twitterUser)

		if user_id is None:
			return []

		#fin de la traduccion
		query = """SELECT orig_tweet, created_at  FROM tweets WHERE tuser = %s ORDER BY id_twitter DESC LIMIT %s;"""
		try:
			rows = self.session_cassandra.execute(query, [user_id, limit])
			if rows is not None:
				return rows
			else:
				return []

		except Exception, e:
			print "getOrigTweetAndCreatedAtFromTweetsByUser"
			print e
			return []

	def getOrigTweetAndCreatedAtFromTweetsByListIDSTweets(self, lista_tweets):
		"""
			retorna un Array de objetos, estos objetos solo contienen el orig_tweet y created_at
			lista_tweets debe ser un array de identificadores de tweets
			Recordemos: 
				created_at es un objeto dateTime
				orig_tweet es 0 si es un tweet del usuario, otro identificador si es un RT
		"""
		query = """SELECT orig_tweet, created_at  FROM tweets WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = []
			for idtwitter in lista_tweets:
				row = self.session_cassandra.execute(query, [idtwitter])
				if row is not None:
					rows.append(row[0])

			return rows
		except Exception, e:
			print "getOrigTweetAndCreatedAtFromTweetsByUser"
			print e
			return []

	def getTweetStatusCassandra(self, identificador):
		"""
			retorna el status del tweet (el texto) dado el identificador del tweet
		"""
		query = "SELECT status FROM tweets WHERE id_twitter = %s LIMIT 1;"
		try:
			rows = self.session_cassandra.execute(query, [identificador])
			row = rows[0]

			return row.status
		except Exception, e:
			print "getTweetStatusCassandra"
			print str(e)
			return False

	def getUserByIDLargeCassandra(self, identificador):
		"""
			Retorna la informacion de un usuario dado un identificador, sobre todo para la interfaz web

			Esta informacion se compone de:
				name
				screen_name
				followers
				location
				created_at
		"""
		query = """SELECT name, screen_name, followers, location, created_at FROM users WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [identificador])
			if rows is not None and len(rows) > 0:
				row = rows[0]
				return row
			else:
				return False
		except Exception, e:
			print "getUserByIDLargeCassandra"
			print str(e)
			return False

	def getUserByIDLargeCassandra_police(self, identificador):
		"""
			Retorna la informacion de un usuario dado un identificador, sobre todo para la interfaz web de la policia

			Esta informacion se compone de:
				name
				screen_name
				followers
				location
				created_at
		"""
		query = """SELECT name, screen_name, followers, following, location, created_at FROM users WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [identificador])
			if rows is not None and len(rows) > 0:
				row = rows[0]
				if row.following is None:
					row.following = 0
				if row.followers is None:
					row.followers = 0
				return row
			else:
				return False
		except Exception, e:
			print "getUserByIDLargeCassandra"
			print str(e)
			return False

	def getUserByIDShortCassandra(self, identificador):
		"""
			Retorna la informacion de un usuario dado un identificador, sobre todo para la interfaz web

			Esta informacion se compone de:
				screen_name
				profile_img
		"""

		query = """SELECT screen_name, profile_img FROM users WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [identificador])
			if rows is not None and len(rows) > 0:
				row = rows[0]
				return row
			else:
				return False
		except Exception, e:
			print "getUserByIDShortCassandra"
			print str(e)
			return False

	def getTweetUserByTweetIDCassandra(self , identificador):
		"""
			Retorna el identificador de usuario dado un identificador de tweet
		"""
		query = "SELECT tuser FROM tweets WHERE id_twitter = %s LIMIT 1;"
		try:
			return self.session_cassandra.execute(query, [identificador])[0].tuser
		except Exception, e:
			print "getTweetUserByTweetIDCassandra"
			print e

	def getTweetByIDLargeCassandra(self, identificador):
		"""
			Retorna la informacion de un tweet completo junto con la informacion del usuario, 
				dado un identificador de tweet
		"""
		query = """SELECT status, favorite_count, retweet_count, orig_tweet, media_urls, tuser, id_twitter FROM tweets WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [identificador])
			row = rows[0]
			user = self.getUserByIDShortCassandra(row.tuser)

			Row = namedtuple('Row', 'status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter')
			retorno = Row(row.status, row.favorite_count, row.retweet_count, row.orig_tweet, row.media_urls, user.screen_name, user.profile_img, row.id_twitter)
			return retorno
		except Exception, e:
			print "getTweetByIDLargeCassandra"
			print str(e)
			return False

	#TODO Problemas de seguridad?
	def getTweetsTopicsCassandra(self, topics, use_max_id=False, max_id=0, limit=100):
		"""
			Realiza una consulta por topic en Cassandra lucene

			El formato de tweet es el común:
				status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter
		"""
		query = "SELECT status, favorite_count, retweet_count, orig_tweet, media_urls, tuser, id_twitter, created_at, lang FROM tweets WHERE lucene =\'{"
		if use_max_id:
			query += "filter : {type:\"boolean\", must:["
			query += "{type:\"match\", field:\"orig_tweet\", value:0}, "
			query += "{type:\"range\", field:\"id_twitter\", upper: "+str(max_id)+", include_upper:false} ] },"
		else:
			query += """filter : {type:\"boolean\", must:[
				   {type:"match", field:"orig_tweet", value:0} ] },"""
		query += "query : {type:\"phrase\", field:\"status\", value:\""+topics+"\", slop:1}, "
		query += "sort : {fields: [ {field:\"created_at\", reverse:true} ] }"
		query += "}\' limit %s;"
		

		Row = namedtuple('Row', 'status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter, created_at, lang')

		try:
			rows = self.session_cassandra.execute(query, [limit])
			retorno = blist([])
			#JOIN
			for row in rows:
				user = self.getUserByIDShortCassandra(row.tuser)
				fila = Row(row.status, row.favorite_count, row.retweet_count, row.orig_tweet, row.media_urls, user.screen_name, user.profile_img, row.id_twitter, row.created_at, row.lang)
				retorno.append(fila)
			return retorno
		except Exception, e:
			print "getTweetsTopicsCassandra"
			print str(e)
			return False

	def getStatusTopicsCassandra(self, topics, limit=100, rts=False):
		"""
			Realiza una consulta por topic en Cassandra lucene

			El formato de tweet es solo el status y el idioma:
				status, lang
		"""
		query = "SELECT status, lang, created_at FROM tweets WHERE lucene =\'{"
		if rts == False:
			query += """filter : {type:\"boolean\", must:[
					   {type:"match", field:"orig_tweet", value:0} ] },"""
		query += "query : {type:\"phrase\", field:\"status\", value:\""+topics+"\", slop:1}, "
		query += "sort : {fields: [ {field:\"created_at\", reverse:true} ] }"
		query += "}\' limit %s;"
		

		try:
			rows = self.session_cassandra.execute(query, [limit])
			return rows
		except Exception, e:
			print "getTweetsTopicsCassandra"
			print str(e)
			return False

	def getUsersHasRetweetedByOrigTweetCassandra(self, identificador):
		query = "SELECT tuser, created_at FROM tweets WHERE orig_tweet = %s;"
		try:
			retorno = blist([])
			rows = self.session_cassandra.execute(query, [identificador])
			for row in rows:
				retorno.append([row.tuser,row.created_at])

			return retorno
		except Exception, e:
			print "getUsersHasRetweetedByOrigTweetCassandra"
			print str(e)
			return False


	#TODO Problemas de seguridad?
	def getIDsTweetsTrainCassandra(self, topics, limit):
		"""
			Realiza una busqueda en Cassandra lucene de identificadores para hacer búsquedas por topics y entrenar en el tfg

			Por ahora solo se usa en el TFG
		"""
		query = "SELECT id_twitter FROM tweets WHERE lucene =\'{"
		query += """filter : {type:\"boolean\", must:[
				   {type:"match", field:"orig_tweet", value:0} ] },"""
		query += "query : {type:\"phrase\", field:\"status\", value:\""+topics+"\", slop:1} "
		query += "}\' limit %s;"

		try:
			return self.session_cassandra.execute(query, [limit])
		except Exception, e:
			print "getTweetsTopicsCassandra"
			print str(e)
			return False


	def getTweetsEntrenamientoListarCassandra(self, identificadores):
		"""
			Por ahora solo se usa en el tfg
		"""
		# entrada [[id_tweet, clase], ...]
		Row = namedtuple('Row', 'status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter, clase')

		try:
			retorno = []

			for tweet_entrenamiento in identificadores:
				tw = self.getTweetByIDLargeCassandra(tweet_entrenamiento[0])
				row = Row(tw.status, tw.favorite_count, tw.retweet_count, tw.orig_tweet, 
					tw.media_urls, tw.screen_name, tw.profile_img, tw.id_twitter,tweet_entrenamiento[1])

				retorno.append(row)

			print retorno
			return retorno
		except Exception, e:
			print str(e)
			return False

	def getAllTweetsNoRtStatusCassandra(self):
		"""
			retorna todos los status de los tweets que no son RT
			Para hacer NLP
		"""
		query = "SELECT status FROM tweets WHERE orig_tweet = 0;"

		try:
			return self.session_cassandra.execute(query)
		except Exception, e:
			print "getAllTweetsStatusCassandra"
			print e

	def getAllIDsTweets(self):
		"""
			Retorna todos los identificadores de todos los tweets,
			Para hacer analisis internos de la base de datos
		"""
		query = "SELECT id_twitter FROM tweets;"
		try:
			rows = self.session_cassandra.execute(query)
			retorno = blist([])
			for row in rows:
				retorno.append(row[0])
			return retorno
		except Exception, e:
			print "getAllIDsTweets"
			print e

	def getAllStatusAndIDUser(self):
		"""
			Retorna status y el identificador de usuario de todos los tweets.

			Para hacer NLP dado un usuario
		"""
		query = "SELECT status, tuser FROM tweets;"
		try:
			return self.session_cassandra.execute(query)
		except Exception, e:
			print "getAllStatusAndIDUser"
			print

	def getAllStatusAndIDUserFiltrateLang(self, lang):
		"""
			Retorna status y el identificador de usuario de todos los tweets.

			Para hacer NLP dado un usuario
		"""
		query = "SELECT status, tuser, lang FROM tweets WHERE lang = %s;"
		try:
			return self.session_cassandra.execute(query, [lang])
		except Exception, e:
			print "getAllStatusAndIDUser"
			print 



	def getAllTweetsNoRtStatusFiltrLangCassandra(self, lang):
		return self.cassandra_spark.getAllTweetsNoRtStatusFiltrLangCS(lang)

	
	def getFollowersByUserID(self, user_id):
		query = "SELECT followers FROM users WHERE id_twitter = %s;"
		try:
			return self.session_cassandra.execute(query, [user_id])
		except Exception, e:
			print "getFollowersByUserID"
			print e

	def getFollowingByUserID(self, user_id):
		query = "SELECT following FROM users WHERE id_twitter = %s;"
		try:
			return self.session_cassandra.execute(query, [user_id])
		except Exception, e:
			print "getFollowingByUserID"
			print e

	"""Sentimientos"""
	def getTweetsTextAndLang(self, lang, limit = 5000000):
		query = "SELECT status, lang FROM tweets WHERE lang = %s AND orig_tweet = 0 Limit %s ALLOW FILTERING;"

		try:
			rows = self.session_cassandra.execute(query, [lang, limit])
			return rows
		except Exception, e:
			print str(e)
			return False

	"""fin de Sentimientos"""

	def getAllUsers(self):
		"""
		Returns
		-------
		lista de usuarios,cada fila tiene id_twitter, screen_name
		"""
		query = "SELECT id_twitter, screen_name FROM users;"
		try:
			rows = self.session_cassandra.execute(query)

			return rows
		except Exception, e:
			print "getAllUsers"
			print e


	"""estadisticas"""
	def getNumTweetsRTCassandra(self):
		return self.cassandra_spark.getNumTweetsRTCS()

	def getNumTweetsMediaCassandra(self):
		return self.cassandra_spark.getNumTweetsMediaCS()

	def getAverageRTMediaCassandra(self):
		return self.cassandra_spark.getAverageRTMediaCS()

	#no_media, si_media
	def getAverageRTMediaByScreenNameCassandra(self, screen_name):
		user_id = self.getUserIDByScreenNameCassandra(screen_name)
		return self.cassandra_spark.getAverageRTMediaByIDUserCS(user_id)

	def getNumTweetsCassandra(self):
		query = "SELECT id_twitter FROM tweets;"
		try:
			rows = self.session_cassandra.execute(query)
			contador = 0
			for row in rows:
				contador += 1

			return contador
		except Exception, e:
			print "getNumTweetsCassandra"
			print e

	def getNumUsersCassandra(self):
		query = "SELECT id_twitter FROM users;"
		try:
			rows = self.session_cassandra.execute(query)
			contador = 0
			for row in rows:
				contador += 1

			return contador
		except Exception, e:
			print "getNumUsersCassandra"
			print e



	"""Fin estadisticas"""
	"""PRUEBAS"""
	def getTweetsUserAndPrintFile(self, filename, twitterUser):
		"""obtiene los tweets y los imprime en un fichero para que se puedan hacer pruebas con los textos"""
		fOut = codecs.open(filename, "w", "utf-8")
		tweets = self.getTweetsUsuarioCassandra(twitterUser, limit=10000)
		for tweet in tweets:
			texto = tweet.status
			texto = texto.replace("\n", " ")
			fOut.write(texto)
			fOut.write("\n")

		fOut.close()

if __name__ == '__main__':
	consultas = ConsultasCassandra()
	print consultas.getNumTweetsCassandra()
	print consultas.getNumUsersCassandra()
	exit()
	print "test de getUserIDByScreenNameCassandra"
	print consultas.getUserIDByScreenNameCassandra("p_molins")
	print "test de getTweetsUsuarioCassandra"
	print consultas.getTweetsUsuarioCassandra("WillyrexYT", limit=10000)[0]
	print consultas.getTweetsUsuarioCassandra("WillyrexYT", use_max_id=True, max_id=611207358266544128, limit=10000)[0]
	print "test de setLastTweetCollectedScreenNameCassandra"
	print consultas.setLastTweetCollectedScreenNameCassandra("WillyrexYT", 0)
	print "test de getLastTweetCollectedScreenNameCassandra"
	print consultas.getLastTweetCollectedScreenNameCassandra("WillyrexYT")
	print "test de getUserByIDLargeCassandra"
	print consultas.getUserByIDLargeCassandra(230377004)
	print consultas.getUserByIDLargeCassandra(230377004)[2]
	print "inspecion de los metodos de row"
	print "Es un namedtuple, por lo que haremos un join a mano"
	print "test de getTweetByIDLargeCassandra"
	print consultas.getTweetByIDLargeCassandra(631260309026553856)
	print "test de getTweetsTopicsCassandra"
	print consultas.getTweetsTopicsCassandra("galletas")[0]
	print consultas.getTweetsTopicsCassandra("@WillyrexYT Esto es mi día a día")[0]
	print consultas.getTweetsTopicsCassandra("galletas", use_max_id=True, max_id=631260309026553856, limit=100)[0]
	print "test de getIDsTweetsTrainCassandra"
	print consultas.getIDsTweetsTrainCassandra("galletas", 100)[0]
	tiempo_inicio = time.time()
	print "test de getNumTweetsRTCassandra"
	print consultas.getNumTweetsRTCassandra()
	tiempo_fin = time.time()
	print tiempo_fin - tiempo_inicio
	print "test de getAverageRTMediaByScreenNameCassandra"
	print consultas.getAverageRTMediaByScreenNameCassandra("WillyrexYT")

	print "Test de seguidores y siguiendo"
	print consultas.getFollowersByUserID(2383366169)
	print consultas.getFollowingByUserID(2383366169)


	testCompleto = False
	if testCompleto == True:
		arrayUsuarios = ["WillyrexYT", "Alvaro845", "Thetoretegg", "Fernanfloo", "Nestle_es", "yuyacst", "AlexMonthy", "Wigetta", "Xodaaaa", "Gameloft_Spain", "NexxuzHD", "AudazCarlos", "xPekeLoL", "steam_games", "vegetta777", "bysTaXx", "bysTaXx", "PlayStationES", "mangelrogel", "Outconsumer"]
		for usuario in arrayUsuarios:
			consultas.getTweetsUserAndPrintFile("/home/dani/ficherosPrueba_plsa/"+usuario+".txt",usuario)