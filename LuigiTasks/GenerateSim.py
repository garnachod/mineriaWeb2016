# -*- coding: utf-8 -*-
import os
import sys
#lib_path = os.path.abspath('/home/dani/github/ConcursoPolicia')
#if lib_path not in sys.path:
#	sys.path.append(lib_path)

import luigi
from RecolectorTwitter import *
from Config.Conf import Conf

from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from DBbridge.ConsultasSQL_police import ConsultasSQL_police

from ProcesadoresTexto.GenerateVectorsFromTweets import GenerateVectorsFromTweets
from AnnoyComparators.AnnoyUserVectorSearcher import AnnoyUserVectorSearcher
import datetime
import numpy as np
import smtplib
from collections import namedtuple

def sendEmail(id_tarea):
	conf = Conf()
	consultas = ConsultasSQL_police()
	if consultas.getSendEmailFromTask(id_tarea) == True:
		id_user = consultas.getIdUserFromTask(id_tarea)

		if id_user != False:
			email = consultas.getEmailFromUser(id_user)
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.ehlo()
			server.starttls()
			fromaddr = "concurso.policia.tareas@gmail.com"
			toaddrs = email
			username = consultas.getUsernameFromTask(id_tarea)
			texto = consultas.getTextFromTask(id_tarea)

			if username:
				asunto = "[Tarea Finalizada] Usuarios similares a " + username + "."
				cuerpo = "La búsqueda de usuarios similares se ha completado." + "Puede consultar los resultados en: http://" + conf.getDomain() + "/resultados/" + str(id_tarea) + "/"
			else:
				asunto = "[Tarea Finalizada] Usuarios similares al texto: " + texto[:20] + "."
				cuerpo = "La búsqueda de usuarios similares a un texto dado se ha completado. Puede consultar los resultados en: http://" + conf.getDomain() + "/resultados/" + str(id_tarea) + "/"

			msg = "\r\n".join([
			  "From: "+ fromaddr,
			  "To: " + toaddrs,
			  "Subject: " + asunto,
			  "",
			  cuerpo
			])
			server.login(fromaddr, "TareasPolicia.sender")
			server.sendmail(fromaddr, toaddrs, msg)
			server.quit()

class GenerateSimAll_topics(luigi.Task):
	usuario = luigi.Parameter()
	lang = luigi.Parameter()
	idtarea = luigi.IntParameter(default=0)

	def requires(self):
		return RecolectorUsuarioTwitter(self.usuario)

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
		return luigi.LocalTarget('%s/LuigiTasks/similitudes/topics_all/%s/%s/%s_%s_%s'%(path, anyo, mes, dia, self.usuario, self.lang))

	def run(self):
		numberOfSim = 5000

		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(self.usuario)
		if len(tweets) < 4:
			with self.output().open('w') as out_file:
				out_file.write("\n")

		#al menos necesitamos 4 tweets para caracterizar a una persona
		#aunque cuantos mas mejor
		else:
			generator = GenerateVectorsFromTweets()
			vector = generator.getVector_topics(tweets, self.lang)
			searcher = AnnoyUserVectorSearcher()
			users = searcher.getSimilarUsers_topics(vector, self.lang, numberOfSim + 1)
			users_long = []
			for user in users:
				user_long = consultas.getUserByIDLargeCassandra_police(user)
				if user_long != False:
					if user_long.screen_name not in self.usuario:
						users_long.append(user)

				if len(users_long) >= numberOfSim:
					break

			with self.output().open('w') as out_file:
				for _user in users_long:
					out_file.write(str(_user))
					out_file.write("\n")


		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.idtarea)
		sendEmail(self.idtarea)

class GenerateSimAll_semantic(luigi.Task):
	usuario = luigi.Parameter()
	lang = luigi.Parameter()
	idtarea = luigi.IntParameter(default=0)

	def requires(self):
		return RecolectorUsuarioTwitter(self.usuario)

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
		return luigi.LocalTarget('%s/LuigiTasks/similitudes/semantic_all/%s/%s/%s_%s_%s'%(path, anyo, mes, dia, self.usuario, self.lang))

	def run(self):
		numberOfSim = 5000

		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsUsuarioCassandra_statusAndLang_noRT(self.usuario)
		if len(tweets) < 4:
			with self.output().open('w') as out_file:
				out_file.write("\n")

		#al menos necesitamos 4 tweets para caracterizar a una persona
		#aunque cuantos mas mejor
		else:
			generator = GenerateVectorsFromTweets()
			vector = generator.getVector_semantic(tweets, self.lang)
			searcher = AnnoyUserVectorSearcher()
			users = searcher.getSimilarUsers_semantic(vector, self.lang, numberOfSim + 1)
			users_long = []
			for user in users:
				user_long = consultas.getUserByIDLargeCassandra_police(user)
				if user_long != False:
					if user_long.screen_name not in self.usuario:
						users_long.append(user)

				if len(users_long) >= numberOfSim:
					break

			with self.output().open('w') as out_file:
				for _user in users_long:
					out_file.write(str(_user))
					out_file.write("\n")

		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.idtarea)
		sendEmail(self.idtarea)

class GenerateSimRelations_semantic(luigi.Task):
	usuario = luigi.Parameter()
	lang = luigi.Parameter()
	idtarea = luigi.IntParameter(default=0)

	def requires(self):
		return RecolectorCirculoUsuario(self.usuario)

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
		return luigi.LocalTarget('%s/LuigiTasks/similitudes/semantic/%s/%s/%s_%s'%(path, anyo, mes, self.usuario, self.lang))

	def run(self):
		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsUsuarioCassandra_statusAndLang_noRT(self.usuario)
		generator = GenerateVectorsFromTweets()
		vector = generator.getVector_semantic(tweets, self.lang)
		#se generan los vectores de todos los usuarios
		consultasNeo4j = ConsultasNeo4j()
		userID = consultas.getUserIDByScreenNameCassandra(self.usuario)
		seguidoresysiguiendo = consultasNeo4j.getSiguiendoOrSeguidosByUserID(userID)
		relaciones_coseno = []
		for user in seguidoresysiguiendo:
			tweets_ = consultas.getTweetsUsuarioCassandra_statusAndLang_noRT(user)
			vector_ = np.array([generator.getVector_semantic(tweets_, self.lang)]).T
			coseno = np.dot(vector, vector_)[0]
			relaciones_coseno.append((user, coseno))

		relaciones_coseno = sorted(relaciones_coseno, key=lambda x: x[1], reverse=True)

		with self.output().open('w') as out_file:
			for relacion in relaciones_coseno:
				out_file.write(str(relacion[0]))
				out_file.write("\n")

		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.idtarea)
		sendEmail(self.idtarea)

class GenerateSimRelations_topics(luigi.Task):
	usuario = luigi.Parameter()
	lang = luigi.Parameter()
	idtarea = luigi.IntParameter(default=0)

	def requires(self):
		return RecolectorCirculoUsuario(self.usuario)

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
		return luigi.LocalTarget('%s/LuigiTasks/similitudes/topic/%s/%s/%s_%s'%(path, anyo, mes, self.usuario, self.lang))

	def run(self):
		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(self.usuario)
		generator = GenerateVectorsFromTweets()
		vector = generator.getVector_topics(tweets, self.lang)
		#se generan los vectores de todos los usuarios
		consultasNeo4j = ConsultasNeo4j()
		userID = consultas.getUserIDByScreenNameCassandra(self.usuario)
		seguidoresysiguiendo = consultasNeo4j.getSiguiendoOrSeguidosByUserID(userID)
		relaciones_coseno = []
		for user in seguidoresysiguiendo:
			tweets_ = consultas.getTweetsUsuarioCassandra_statusAndLang(user)
			vector_ = np.array([generator.getVector_topics(tweets_, self.lang)]).T
			coseno = np.dot(vector, vector_)[0]
			relaciones_coseno.append((user, coseno))

		relaciones_coseno = sorted(relaciones_coseno, key=lambda x: x[1], reverse=True)

		with self.output().open('w') as out_file:
			for relacion in relaciones_coseno:
				out_file.write(str(relacion[0]))
				out_file.write("\n")

		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.idtarea)
		sendEmail(self.idtarea)

class GenerateSimText_topics(luigi.Task):
	idtarea = luigi.IntParameter()
	lang = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget('%s/LuigiTasks/similitudes/topic/%s/%s/%s_%s'%(path, anyo, mes, self.idtarea, self.lang))

	def run(self):
		consultas = ConsultasSQL_police()
		#714
		text = consultas.getTextFromTask(self.idtarea)
		text = text.decode('utf-8', 'ignore')
		#print text
		if text == False:
			with self.output().open('w') as out_file:
				out_file.write("\n")

		else:
			Row = namedtuple('Row', 'status, lang')
			tweets = [Row(text, self.lang)]
			generator = GenerateVectorsFromTweets()
			vector = generator.getVector_topics(tweets, self.lang)
			#print vector
			searcher = AnnoyUserVectorSearcher()
			users = searcher.getSimilarUsers_topics(vector, self.lang, 5000)

			with self.output().open('w') as out_file:
				for user in users:
					out_file.write(str(user))
					out_file.write("\n")

		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.idtarea)
		sendEmail(self.idtarea)

class GenerateSimText_semantic(luigi.Task):
	idtarea = luigi.IntParameter()
	lang = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget('%s/LuigiTasks/similitudes/semantic/%s/%s/%s_%s'%(path, anyo, mes, self.idtarea, self.lang))

	def run(self):
		consultas = ConsultasSQL_police()
		text = consultas.getTextFromTask(self.idtarea)
		text = text.decode('utf-8', 'ignore')
		if text == False:
			with self.output().open('w') as out_file:
				out_file.write("\n")
		else:
			Row = namedtuple('Row', 'status, lang')
			tweets = [Row(text, self.lang)]
			generator = GenerateVectorsFromTweets()
			vector = generator.getVector_semantic(tweets, self.lang)
			searcher = AnnoyUserVectorSearcher()
			users = searcher.getSimilarUsers_semantic(vector, self.lang, 5000)

			with self.output().open('w') as out_file:
				for user in users:
					out_file.write(str(user))
					out_file.write("\n")

		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.idtarea)
		sendEmail(self.idtarea)
