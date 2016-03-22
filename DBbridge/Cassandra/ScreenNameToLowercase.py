from Cassandra.ConexionCassandra import ConexionCassandra

if __name__ == '__main__':

	session_cassandra = ConexionCassandra().getSession()
	query_all_users = """ SELECT id_twitter, screen_name from users;"""
	query_insert = """INSERT INTO users (id_twitter, screen_name)
				   		VALUES (%s, %s);
					"""

	rows = session_cassandra.execute(query_all_users)
	for i, row in enumerate(rows):
		id_twitter = row.id_twitter
		screen_name = row.screen_name.lower()
		session_cassandra.execute(query_insert, [id_twitter, screen_name])
		if i % 50000 == 0: print i
		if i % 5000 == 0: print screen_name