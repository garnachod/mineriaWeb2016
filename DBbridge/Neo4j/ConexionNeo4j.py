from Config.Conf import Conf
from py2neo import Graph,authenticate


class ConexionNeo4j(object):
	"""docstring for ConexionNeo4j"""

	class __impl:
		""" Implementation of the singleton interface """

		def __init__(self):
			authenticate("localhost:7474", "neo4j", Conf().getNeo4jPassword())
			self.graph = Graph()
			
		def getGraph(self):
			return self.graph

	# storage for the instance reference
	__instance = None

	def __init__(self):
		if ConexionNeo4j.__instance is None:
			ConexionNeo4j.__instance = ConexionNeo4j.__impl()

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)