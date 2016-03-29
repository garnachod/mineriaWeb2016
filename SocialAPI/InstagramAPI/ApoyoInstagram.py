# -*- coding: utf-8 -*-
from DBbridge.ConsultasInstagram import ConsultasInstagram


class ApoyoInstagram(object):
	"""docstring for ApoyoInstagram"""
	def __init__(self):
		super(ApoyoInstagram, self).__init__()
		self.consultas = ConsultasInstagram()

	def isUserInDBByUsername(self, username):
		"""
			Retorna el id si el usuario está en la base de datos
			Retorna False si no está en la base de datos
		"""
		id = self.consultas.getIDByUsername(username)
		if id is not None:
			return id.id
		else:
			return False

	def isUserCompleteInDBByUsername(self, username):
		"""
			Retorna True si el usuario está en la base de datos y completo
			Retorna False si no está en la base de datos completo
		"""
		user = self.consultas.getUserLongByUserName(username)
		if user is not None:
			#comprueba si está completo ahora
			if user.followers is not None:
				return True
			else:
				return False
		else:
			return False