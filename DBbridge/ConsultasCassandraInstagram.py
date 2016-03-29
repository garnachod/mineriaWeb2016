# -*- coding: utf-8 -*-
from Cassandra.ConexionCassandra import ConexionCassandra
from collections import namedtuple
from blist import blist

"""
'CREATE TABLE users ('
             'id bigint PRIMARY KEY'
             ', username varchar'
             ', full_name varchar'
             ', followers int'
             ', following int'
             ', bio varchar'
             ', profile_picture varchar'
             ', last_media_collected bigint);'
"""

class ConsultasCassandraInstagram(object):
	"""docstring for ConsultasCassandraInstagram"""
	def __init__(self):
		super(ConsultasCassandraInstagram, self).__init__()
		self.session_cassandra = ConexionCassandra().getSessionInstagram()

	
	def getUserLongByID(self, identificador):
		"""
			retorna toda la informacion del usuario dado un identificador
		"""
		pass

	def getUserLongByUserName(self, username):
		"""
			retorna la informacion relevante al exterior de la app del usuario dado un nombre de usuario
		"""
		query = """SELECT id, username, full_name, followers, following, bio, profile_picture FROM users WHERE username = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [username])
			if len(rows) == 0:
				return None

			return rows[0]
		except Exception, e:
			print "getUserIDByScreenNameCassandra"
			print e
			return None

	def getIDByUsername(self, username):
		"""
			retorna el id del usuario dado un nombre de usuario
		"""
		query = """SELECT id FROM users WHERE username = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [username])
			if len(rows) == 0:
				return None

			return rows[0]
		except Exception, e:
			print "getUserIDByScreenNameCassandra"
			print e
			return None

if __name__ == '__main__':
	print ConsultasCassandraInstagram().getUserLongByUserName("garnachod")