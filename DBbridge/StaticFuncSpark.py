from Cassandra.ConexionCassandra import ConexionCassandra

class StaticFuncSpark(object):
	
	@staticmethod
	def getTweetsAndCount(tupla):
			session_cassandra = ConexionCassandra().getSession()
			x, y = tupla
			rows = None
			if x == 0:
				query = "SELECT orig_tweet FROM tweets WHERE id_twitter <= %s ALLOW FILTERING;"
				#query = "SELECT orig_tweet FROM tweets WHERE lucene=\'{"
				#query += "filter : {type:\"range\", field:\"id_twitter\", lower:"+str(y)+", upper:"+str(0)+"}"
				#query += "}';"
				rows = session_cassandra.execute(query, [y])
				#rows = session_cassandra.execute(query)
			if y == 0:
				query = "SELECT orig_tweet FROM tweets WHERE id_twitter > %s ALLOW FILTERING;"
				#query = "SELECT orig_tweet FROM tweets WHERE lucene=\'{"
				#query += "filter : {type:\"range\", field:\"id_twitter\", lower:"+str(2**32)+", upper:"+str(x)+"}"
				#query += "}';"
				rows = session_cassandra.execute(query, [x])
				#rows = session_cassandra.execute(query)
			else:
				query = "SELECT orig_tweet FROM tweets WHERE id_twitter > %s AND id_twitter <= %s ALLOW FILTERING;"
				#query = "SELECT orig_tweet FROM tweets WHERE lucene=\'{"
				#query += "filter : {type:\"range\", field:\"id_twitter\", lower:"+str(y)+", upper:"+str(x)+"}"
				#query += "}';"
				rows = session_cassandra.execute(query, [x, y])
				#rows = session_cassandra.execute(query)

			count_no_rt = 0
			count_si_rt = 0
			for row in rows:
				if row[0] == 0:
					count_no_rt += 1
				else:
					count_si_rt += 1

			return [("no_rt", count_no_rt), ("si_rt", count_si_rt)]
		