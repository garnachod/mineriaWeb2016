# -*- coding: utf-8 -*-
import os
import sys
#lib_path = os.path.abspath('../../')
#sys.path.append(lib_path)
from DBbridge.EscritorUsuariosInstagramCassandra import EscritorUsuariosInstagramCassandra
from DBbridge.EscritorSeguidoresInstagramNeo4j import EscritorSeguidoresInstagramNeo4j

from SocialAPI.Recolector import Recolector
from GetAuthorizations import GetAuthorizations
from instagram.client import InstagramAPI
from RecolectorUsuario import RecolectorUsuario
from ApoyoInstagram import ApoyoInstagram
from time import time

class RecolectorSeguidores(Recolector):
	"""RecolectorSeguidores necesita un escritor de usuarios y un escritor de relaciones"""
	def __init__(self, escritor):
		super(RecolectorSeguidores, self).__init__(escritor)
		self.authorizator = GetAuthorizations(4999)
		self.apoyo = ApoyoInstagram()
		self.api = None
		self.inicializa()

	def inicializa(self):
		self.authorizator.load_token()
		client_id, client_secret = self.authorizator.get_secret()
		self.api = InstagramAPI(client_id=client_id, client_secret=client_secret)

	def recolecta(self, query):
		id = False
		try:
			id = long(query)
		except Exception, e:
			id = self.apoyo.isUserInDBByUsername(query)
		
		"""Para simplificar el disenno se deja como tarea al usuario descargar antes"""
		if id == False:
			raise Exception('El usuario debe estar en la base de datos')

		follows = self.privateRealizaConsulta_id(id)

		lista_relaciones = []
		for user in follows:
			lista_relaciones.append((user.id, id))

		#print lista_relaciones
		self.guarda(lista_relaciones, follows)


	def guarda(self, relaciones, usuarios):
		for escritor in self.escritores:
			if "EscritorUsuarios" in escritor.__class__.__name__:
				escritor.escribe(usuarios)
			else:
				escritor.escribe(relaciones)


	def privateRealizaConsulta_id(self, identificador):
		if self.authorizator.is_limit_api():
			raise Exception('LIMITE')

		try:
			follows, next_ = self.api.user_followed_by(identificador)

			self.authorizator.add_query_to_key()
			while next_:
				if self.authorizator.is_limit_api():
					raise Exception('LIMITE')

				more_follows, next_ = self.api.user_followed_by(with_next_url=next_)
				self.authorizator.add_query_to_key()
				follows.extend(more_follows)

			return follows
		except Exception, e:
			self.authorizator.add_query_to_key()
			if "429" in str(e):
				raise Exception('LIMITE')
			print e
			return []



if __name__ == '__main__':
	recolector = RecolectorSeguidores([EscritorUsuariosInstagramCassandra(-1), EscritorSeguidoresInstagramNeo4j(-1)])
	recolector.recolecta("garnachod")