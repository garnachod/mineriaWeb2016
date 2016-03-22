from Escritor import Escritor
from Cassandra.ConexionCassandra import ConexionCassandra
import datetime
class EscritorTweetsCassandra(Escritor):
	"""docstring for EscritorTweetsCassandra"""
	def __init__(self, searchID):
		super(EscritorTweetsCassandra, self).__init__(searchID)
		self.session = ConexionCassandra().getSession()
		self.escritorUsrs = EscritorTweetsUsersCassandra(searchID)
		self.asinc = True
		
		
	def escribe(self, data):
		for tweet in data:
			self.escribeTweet(tweet)
			self.escribeUser(tweet["user"])
			
			if "retweeted_status" in tweet:
				self.escribeTweet(tweet["retweeted_status"])
				self.escribeUser(tweet["retweeted_status"]["user"])

	def escribeTweet(self, data):
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

		mediaWrite = {}
		mediaTypeCount = {}
		#guarda todos los links a media que tiene el tweet
		#como puede haber mas de un tipo de media, por ejemplo fotos, se guardan como photo_1, photo_2
		if "entities" in data:
			if "media" in data["entities"]:
				for media in data["entities"]["media"]:
					if media["type"] in mediaTypeCount:
						mediaTypeCount[media["type"]] += 1
					else: 
						mediaTypeCount[media["type"]] = 1

					mediaTag = media["type"] + "_" + str(mediaTypeCount[media["type"]])
					mediaWrite[mediaTag] = media["media_url_https"]
		#Geolocalizacion
		longitud = 0.0
		latitud = 0.0
		if "geo" in data:
			if data["geo"] is not None:
				if data["geo"]["type"] == "Point":
					latitud = float(data["geo"]["coordinates"][0])
					longitud = float(data["geo"]["coordinates"][1])




		query = """INSERT INTO Tweets (id_twitter, status, tuser, created_at, lang, orig_tweet, favorite_count, retweet_count, media_urls, latitude, longitude)
				   VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)
				"""
		try:
			if self.asinc:
				self.session.execute_async(query,
					(identificador, text, user_id, created_at, lang, rt_id, favorite_count, retweet_count, mediaWrite, latitud, longitud))
			else:
				self.session.execute(query,
					(identificador, text, user_id, created_at, lang, rt_id, favorite_count, retweet_count, mediaWrite, latitud, longitud))
		except Exception, e:
			print e
			print identificador
			print text
			print user_id
			print created_at
			print lang
			print rt_id
			print favorite_count
			print retweet_count
			print mediaWrite
			print latitud
			print longitud
			
	def escribeUser(self, user):
		self.escritorUsrs.escribe(user)
					

class EscritorTweetsUsersCassandra(Escritor):
	"""docstring for EscritorTweetsCassandra"""
	def __init__(self, searchID):
		super(EscritorTweetsUsersCassandra, self).__init__(searchID)
		self.session = ConexionCassandra().getSession()
		self.asinc = True
		

	def escribe(self, data):
		""" admite un solo usuario por escritura """
		identificador = data["id"]
		#name
		name = data["name"]
		#screen name
		screen_name = data["screen_name"]
		screen_name = screen_name.lower()
		#location
		location = data["location"]
		#followers_count
		followers_count = data["followers_count"]
		#friends_count
		friends_count = data["friends_count"]
		#created_at
		created_at = datetime.datetime.strptime(data["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
		#url_img_user
		url_img_user = data["profile_image_url_https"]

		query = """INSERT INTO users (id_twitter, name, screen_name, created_at, followers, location, profile_img, following)
				   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
				"""
		try:
			if self.asinc:
				self.session.execute_async(query,
					(identificador, name, screen_name, created_at, followers_count, location, url_img_user, friends_count))
			else:
				self.session.execute(query,
					(identificador, name, screen_name, created_at, followers_count, location, url_img_user, friends_count))
		except Exception, e:
			print e
