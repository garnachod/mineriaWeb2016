# -*- coding: utf-8 -*-
try:
	from cassandra.cluster import Cluster
except:
	pass
from Config.Conf import Conf

class ConexionCassandra():
	"""docstring for ConexionCassandra"""

	class __impl:
		""" Implementation of the singleton interface """

		def __init__(self):
			cluster_cass = Cluster()
			self.session = cluster_cass.connect(Conf().getCassandraKeyspace())
			self.session.default_timeout = 100
			self.session_instagram = cluster_cass.connect(Conf().getCassandraKeyspaceInstagram())

		def getSession(self):
			""" Test method, return singleton conexion"""
			return self.session

		def getSessionInstagram(self):
			""" Test method, return singleton conexion"""
			return self.session_instagram


	# storage for the instance reference
	__instance = None

	def __init__(self):
		if ConexionCassandra.__instance is None:
			ConexionCassandra.__instance = ConexionCassandra.__impl()

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)
