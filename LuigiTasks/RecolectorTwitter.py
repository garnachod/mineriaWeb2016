# -*- coding: utf-8 -*-
import os
import sys


from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from DBbridge.EscritorSeguidoresNeo4j import EscritorSeguidoresNeo4j
from DBbridge.EscritorFavoritosNeo4j import EscritorFavoritosNeo4j
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from DBbridge.ConsultasCassandra import ConsultasCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsStatusStream import RecolectorTweetsStatusStream
from SocialAPI.TwitterAPI.RecolectorTweetsUsersStream import RecolectorTweetsUsersStream
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
from SocialAPI.TwitterAPI.RecolectorFavoritosUser import RecolectorFavoritosUser
from SocialAPI.TwitterAPI.RecolectorSiguiendoShort import RecolectorSiguiendoShort
from SocialAPI.TwitterAPI.RecolectorSeguidoresShort import RecolectorSeguidoresShort
import luigi
from time import time, sleep
from Config.Conf import Conf
import datetime
class RecolectorUsuarioTwitter(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		try:
			usuario = self.usuario.replace("@", "")
			self.usuario = usuario
		except:
			pass
		return luigi.LocalTarget('%s/LuigiTasks/users/%s/%s/%s/%s'%(path, anyo, mes, dia, self.usuario))

	def run(self):
		"""
		Realiza una busqueda en TwitterAPI

		Recolecta los tweets de un usuario dado por nombre de usuario
		o identificador
		"""
		escritorList = []
		escritorList.append(EscritorTweetsCassandra(-1))
		recolector = RecolectorTweetsUser(escritorList)

		while True:
			try:
				identificador = 0
				try:
					identificador = long(self.usuario)
				except Exception, e:
					pass	
				print "descargando"
				if identificador == 0:
					recolector.recolecta(query=self.usuario)
				else:
					recolector.recolecta(identificador=identificador)

				break
			except Exception, e:
				if "LIMITE" in e:
					sleep(1*60)
				else:
					raise e

		with self.output().open('w') as out_file:
			out_file.write("OK")

class RecolectorContenidoTweet(luigi.Task):
	"""
		Realiza una busqueda en TwitterAPI

		Recolecta los tweets que contienen la busqueda, pueden ser hastags, menciones o lo que sea
		default 1.000.000 tardara unas 6 horas si existen ese millon o twiter nos los da
		si el limite es -1 no habra limite (MUCHO CUIDADO)

		OTRO MUCHO CUIDADO
			LUIGI no admite # en la entrada de parametros, no pasa nada, borradlos
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorContenidoTweet --busqueda ... --limitedescarga ...
	"""
	busqueda = luigi.Parameter()
	limitedescarga = luigi.Parameter(default="1000000")

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		hour = now.hour
		return luigi.LocalTarget('%s/LuigiTasks/contenido/%s/%s/%s/%s/%s'%(path, anyo, mes, dia, hour, self.busqueda))

	def run(self):
		escritorList = []
		escritorList.append(EscritorTweetsCassandra(-1))
		recolector = RecolectorTweetsTags(escritorList)
		limite = 1000000
		try:
			limite = int(self.limitedescarga)
		except Exception, e:
			limite = 1000000
		if limite == -1:
			limite = 10000000

		try:
			#recoleccion pura y dura
			for busq in self.busqueda.replace(" ", "").split(","):
				recolector.recolecta(busq, limite = limite)
		except Exception, e:
			if "LIMITE" in e:
				sleep(1*60)
			else:
				raise e

		with self.output().open('w') as out_file:
			out_file.write("OK")

class RecolectorSeguidoresTwitter(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorSeguidoresTwitter --usuario ...
	"""
	usuario = luigi.Parameter()
	forcecomplete = luigi.Parameter(default="True")

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		try:
			usuario = self.usuario.replace("@", "")
			self.usuario = usuario
		except:
			pass
		return luigi.LocalTarget('%s/LuigiTasks/seguidores/%s/%s/%s'%(path, anyo, mes, self.usuario))
		#return luigi.LocalTarget('tasks/RecolectorSeguidoresTwitter(%s)'%self.usuario)

	def requires(self):
		return RecolectorUsuarioTwitter(self.usuario)

	def run(self):
		"""
		Realiza una busqueda en TwitterAPI

		Recolecta los seguidores de un usuario dado por nombre de usuario
		o identificador
		"""
		escritores = [EscritorSeguidoresNeo4j(-1)]
		recolector = RecolectorSeguidoresShort(escritores)
		while True:
			try:
				identificador = 0
				try:
					identificador = long(self.usuario)
				except Exception, e:
					pass	

				if identificador == 0:
					if self.forcecomplete == "True":
						recolector.recolecta(query = self.usuario, complete = True)
					else:
						recolector.recolecta(query = self.usuario)
				else:
					recolector.recolecta(id_user = identificador)
				break
			except Exception, e:
				if "LIMITE" in e:
					sleep(1*60)
				#else:
				#	raise e

		with self.output().open('w') as out_file:
			out_file.write("OK")


class RecolectorSiguiendoTwitter(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		try:
			usuario = self.usuario.replace("@", "")
			self.usuario = usuario
		except:
			pass
		return luigi.LocalTarget('%s/LuigiTasks/siguiendo/%s/%s/%s'%(path, anyo, mes, self.usuario))

	def requires(self):
		return RecolectorUsuarioTwitter(self.usuario)

	def run(self):
		"""
		Realiza una busqueda en TwitterAPI

		Recolecta los siguiendos de un usuario dado por nombre de usuario
		o identificador
		"""
		escritores = [EscritorSeguidoresNeo4j(-1)]
		recolector = RecolectorSiguiendoShort(escritores)
		while True:
			try:
				identificador = 0
				try:
					identificador = long(self.usuario)
				except Exception, e:
					pass	

				if identificador == 0:
					recolector.recolecta(query=self.usuario)
				else:
					recolector.recolecta(id_user=identificador)
				break
			except Exception, e:
				if "LIMITE" in e:
					sleep(1*60)
				else:
					raise e

		with self.output().open('w') as out_file:
			out_file.write("OK")
		

class RecolectorFavoritosTwitter(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		try:
			usuario = self.usuario.replace("@", "")
			self.usuario = usuario
		except:
			pass
		return luigi.LocalTarget('%s/LuigiTasks/favoritos/%s/%s/%s'%(path, anyo, mes, self.usuario))

	def run(self):
		"""
		Realiza una busqueda en TwitterAPI

		Recolecta los favoritos de un usuario dado por nombre de usuario
		o identificador
		"""
		escritores = [EscritorFavoritosNeo4j(-1), EscritorTweetsCassandra(-1)]
		recolector = RecolectorFavoritosUser(escritores)
		while True:
			try:
				identificador = 0
				try:
					identificador = long(self.usuario)
				except Exception, e:
					pass	

				if identificador == 0:
					recolector.recolecta(query=self.usuario)
				else:
					recolector.recolecta(id_user=identificador)
				break
			except Exception, e:
				print e
				sleep(1*60)

		with self.output().open('w') as out_file:
			out_file.write("OK")

class RecolectorTweetsSiguendoTwitter(luigi.Task):
	"""
		Recolecta en un primer momento los siguiendo de un usuario
		a continuacion descarga todos los tweets de esos siguiendo
	"""
	usuario = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		try:
			usuario = self.usuario.replace("@", "")
			self.usuario = usuario
		except:
			pass
		return luigi.LocalTarget('%s/LuigiTasks/TweetsSiguendo/%s/%s/%s'%(path, anyo, mes, self.usuario))

	def requires(self):
		return [RecolectorUsuarioTwitter(self.usuario), RecolectorSiguiendoTwitter(self.usuario)]

	def run(self):
		consultasNeo4j = ConsultasNeo4j()
		consultasCassandra = ConsultasCassandra()

		# si no es un identificador, se intenta conseguir desde cassandra
		identificador = 0
		try:
			identificador = long(self.usuario)
		except Exception, e:
			if self.usuario[0] == "@":
				self.usuario = self.usuario[1:]
			identificador = consultasCassandra.getUserIDByScreenNameCassandra(self.usuario)

		#solo puede no existir ese identificador si es privado, pero debemos controlarlo
		if identificador > 0:
			siguiendos = consultasNeo4j.getListaIDsSiguiendoByUserID(identificador)
			for siguiendo in siguiendos:
				yield RecolectorUsuarioTwitter(siguiendo)

		with self.output().open('w') as out_file:
			out_file.write("OK")


class RecolectorTweetsSeguidoresTwitter(luigi.Task):
	"""
		Recolecta en un primer momento los siguiendo de un usuario
		a continuacion descarga todos los tweets de esos siguiendo
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorTweetsSeguidoresTwitter --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		try:
			usuario = self.usuario.replace("@", "")
			self.usuario = usuario
		except:
			pass
		return luigi.LocalTarget('%s/LuigiTasks/TweetsSeguidores/%s/%s/%s'%(path, anyo, mes, self.usuario))

	def requires(self):
		return [RecolectorUsuarioTwitter(self.usuario), RecolectorSeguidoresTwitter(self.usuario)]

	def run(self):
		consultasNeo4j = ConsultasNeo4j()
		consultasCassandra = ConsultasCassandra()

		# si no es un identificador, se intenta conseguir desde cassandra
		identificador = 0
		try:
			identificador = long(self.usuario)
		except Exception, e:
			if self.usuario[0] == "@":
				self.usuario = self.usuario[1:]
			identificador = consultasCassandra.getUserIDByScreenNameCassandra(self.usuario)

		#solo puede no existir ese identificador si es privado, pero debemos controlarlo
		if identificador > 0:
			seguidores = consultasNeo4j.getListaIDsSeguidoresByUserID(identificador)
			for seguidor in seguidores:
				yield RecolectorUsuarioTwitter(seguidor)

		with self.output().open('w') as out_file:
			out_file.write("OK")


class RecolectorCirculoUsuario(luigi.Task):
	usuario = luigi.Parameter()

	def requires(self):
		return [RecolectorTweetsSeguidoresTwitter(self.usuario), RecolectorTweetsSiguendoTwitter(self.usuario)]

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		try:
			usuario = self.usuario.replace("@", "")
			self.usuario = usuario
		except:
			pass
		return luigi.LocalTarget('%s/LuigiTasks/circulo/%s/%s/%s'%(path, anyo, mes, self.usuario))

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
		

		
if __name__ == "__main__":
	luigi.run()