import psycopg2
from Config.Conf import Conf

class ConexionSQL(): 
	"""docstring for ConexionSQL"""

	class __impl:
		""" Implementation of the singleton interface """

		def __init__(self):
			infoSQL = Conf().getSQLInfo()
			self.conn = psycopg2.connect(database=infoSQL.database, user=infoSQL.user, password=infoSQL.password, host=infoSQL.host)
			infoSQL = Conf().getSQLPoliceInfo()
			self.policeConn = psycopg2.connect(database=infoSQL.database, user=infoSQL.user, password=infoSQL.password, host=infoSQL.host)
		def getConexion(self):
			""" Test method, return singleton conexion"""
			return self.conn

		def getCursor(self):
			return self.conn.cursor()

		def getConexion_police(self):
			""" Test method, return singleton conexion"""
			return self.policeConn

		def getCursor_police(self):
			try:
				return self.policeConn.cursor()
			except:
				infoSQL = Conf().getSQLPoliceInfo()
				self.policeConn = psycopg2.connect(database=infoSQL.database, user=infoSQL.user, password=infoSQL.password, host=infoSQL.host)
				return self.policeConn.cursor()

	# storage for the instance reference
	__instance = None

	def __init__(self):
		if ConexionSQL.__instance is None:
			ConexionSQL.__instance = ConexionSQL.__impl()

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)
		
