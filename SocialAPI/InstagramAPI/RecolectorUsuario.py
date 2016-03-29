# -*- coding: utf-8 -*-
import os
import sys
#lib_path = os.path.abspath('../../')
#sys.path.append(lib_path)
from DBbridge.EscritorUsuariosInstagramCassandra import EscritorUsuariosInstagramCassandra

from SocialAPI.Recolector import Recolector
from GetAuthorizations import GetAuthorizations
from instagram.client import InstagramAPI
from ApoyoInstagram import ApoyoInstagram
from time import time

class RecolectorUsuario(Recolector):
	"""
		Recolecta la información del usuario dado un nombre de usuario,
		Es muy importante porque todas las queries en Instagram usan id y no nombre.
		Por lo que es necesario hacer un patrón proxy
	"""
	def __init__(self, escritor):
		super(RecolectorUsuario, self).__init__(escritor)
		self.authorizator = GetAuthorizations(4999)
		self.apoyo = ApoyoInstagram()
		self.api = None
		self.inicializa()

	def inicializa(self):
		self.authorizator.load_token()
		client_id, client_secret = self.authorizator.get_secret()
		self.api = InstagramAPI(client_id=client_id, client_secret=client_secret)


	def recolecta(self, query, forceDownload = False):
		"""
			Implementado proxy
			por ahora solo admite un usuario por nombre de usuario
		"""
		id = self.apoyo.isUserInDBByUsername(query)
		if id == False:
			usuariosArray = self.privateRealizaConsulta(query)
			self.guarda(usuariosArray)
		else:
			if self.apoyo.isUserCompleteInDBByUsername(query) == True:
				if forceDownload == True:
					usuariosArray = self.privateRealizaConsulta_id(id)
					self.guarda(usuariosArray)
			else:
				usuariosArray = self.privateRealizaConsulta_id(id)
				self.guarda(usuariosArray)

	def guarda(self, arrayDatos):
		#if len(self.escritores) == 0:
		#	print arrayDatos

		for escritor in self.escritores:
			escritor.escribe(arrayDatos)

	def privateRealizaConsulta(self, query):
		if self.authorizator.is_limit_api():
			raise Exception('LIMITE')

		try:
			users = self.api.user_search(q=query, count="1")
			if len(users) <= 0:
				return []
			user = users[0]
			identificador = user.id
			self.authorizator.add_query_to_key()
			usuarioFinal = self.api.user(identificador)
			self.authorizator.add_query_to_key()
			return [usuarioFinal]

		except Exception, e:
			self.authorizator.add_query_to_key()
			print e
			if "429" in str(e):
				raise Exception('LIMITE')
			return []

	def privateRealizaConsulta_id(self, identificador):
		if self.authorizator.is_limit_api():
			raise Exception('LIMITE')

		try:
			usuarioFinal = self.api.user(identificador)
			self.authorizator.add_query_to_key()
			return [usuarioFinal]

		except Exception, e:
			self.authorizator.add_query_to_key()
			if "429" in str(e):
				raise Exception('LIMITE')
			return []


if __name__ == '__main__':
	recolector = RecolectorUsuario([EscritorUsuariosInstagramCassandra(-1)])
	recolector.recolecta("garnachod")