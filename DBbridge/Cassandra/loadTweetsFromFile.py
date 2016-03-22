from ConexionCassandra import ConexionCassandra
import codecs
import datetime
import json

if __name__ == '__main__':
	session_cassandra = ConexionCassandra().getSession()
	fin = codecs.open("/media/dani/data/tweets.txt", "r", "utf-8")
	seps = "(|%;%|)"
	query = """INSERT INTO Tweets (id_twitter, status, tuser, created_at, lang, orig_tweet, favorite_count, retweet_count, media_urls, latitude, longitude)
				   VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"""

	try:
		i = 0
		line = fin.readline()
		while line != "":
			i += 1
			if i % 10000 == 0:
				print i
			line_sp = line.split(seps)
			while len(line_sp) != 12:
				line += fin.readline()
				line_sp = line.split(seps)
			#len == 12


			#query = "SELECT id_twitter, status, tuser, created_at, lang, orig_tweet, favorite_count, retweet_count, media_urls, latitude, longitude FROM tweets;"
			#print line
			media =	None
			try:
				#print line_sp[8].replace("u'", "").replace("'", "")
				media = json.loads(line_sp[8].replace("u'", "\"").replace("'", "\""))
			except Exception, e:
				pass

			session_cassandra.execute(query,
						(long(line_sp[0]), line_sp[1], long(line_sp[2]), datetime.datetime.strptime(line_sp[3], "%Y-%m-%d %H:%M:%S")
							, line_sp[4], long(line_sp[5]), int(line_sp[6]), int(line_sp[7]), media, float(line_sp[9]), float(line_sp[10])))
			
			line = fin.readline()
	except Exception, e:
		print i
		print line
		print e