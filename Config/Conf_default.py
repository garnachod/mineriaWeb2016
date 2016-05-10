from collections import namedtuple

class Conf():
	"""docstring for Conf"""
	class __impl:
		"""docstring for __impl"""
		def __init__(self):
			#dominio web (sin "http://" ni "/" final)
			self.domain = '0.0.0.0:8000'

			#dominio web (sin "http://" ni "/" final)

			#cassandra
			self.cassandra_keyspace = ''
			self.cassandra_keyspace_instagram = ''
			#SQL
			self.sql_database = ''
			self.sql_database_policia = ''
			self.sql_user = ''
			self.sql_password = ''
			self.sql_host = ''
			self.sql_port = ''
			#app
			self.abspath = ''
			#SPARK
			self.spark_home = ''
			#Neo4j
			self.neo4j_password = ''
			#vectors
			self.dimVectors = 50

		def getDomain(self):
			return self.domain

		def getCassandraKeyspace(self):
			return self.cassandra_keyspace

		def getCassandraKeyspaceInstagram(self):
			return self.cassandra_keyspace_instagram

		def getSparkHome(self):
			return self.spark_home

		def getAbsPath(self):
			return self.abspath

		def getSQLInfo(self):
			infoSQL = namedtuple('InfoSQL', 'database, user, password, host')
			return infoSQL(self.sql_database, self.sql_user, self.sql_password, self.sql_host)

		def getSQLPoliceInfo(self):
			infoSQL = namedtuple('InfoSQL', 'database, user, password, host, port')
			return infoSQL(self.sql_database_policia, self.sql_user, self.sql_password, self.sql_host, self.sql_port)

		def getNeo4jPassword(self):
			return self.neo4j_password

		def getDimVectors(self):
			return self.dimVectors



	# storage for the instance reference
	__instance = None

	def __init__(self):
		if Conf.__instance is None:
			Conf.__instance = Conf.__impl()

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)
