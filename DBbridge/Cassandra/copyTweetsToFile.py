from ConexionCassandra import ConexionCassandra
import codecs

import gzip


if __name__ == '__main__':
	session_cassandra = ConexionCassandra().getSession()
	query = "SELECT id_twitter, status, tuser, created_at, lang, orig_tweet, favorite_count, retweet_count, media_urls, latitude, longitude FROM tweets;"
	rows = session_cassandra.execute(query)
	fOut = gzip.open("/media/dani/data/tweets.txt.gz", 'wb')
	seps = "(|%;%|)"
	for row in rows:
		fOut.write(str(row.id_twitter))
		fOut.write(seps)
		fOut.write(row.status.replace(seps, " ").replace("\n", ". ").replace("\r", ". ").replace(u"\u0085", ". ").replace(u"\u2028", ". ").replace(u"\u2029", ". ").encode('utf-8'))
		fOut.write(seps)
		fOut.write(str(row.tuser))
		fOut.write(seps)
		fOut.write(str(row.created_at))
		fOut.write(seps)
		fOut.write(str(row.lang))
		fOut.write(seps)
		fOut.write(str(row.orig_tweet))
		fOut.write(seps)
		fOut.write(str(row.favorite_count))
		fOut.write(seps)
		fOut.write(str(row.retweet_count))
		fOut.write(seps)
		fOut.write(str(row.media_urls))
		fOut.write(seps)
		fOut.write(str(row.latitude))
		fOut.write(seps)
		fOut.write(str(row.longitude))
		fOut.write("\n")

	fOut.close()
	