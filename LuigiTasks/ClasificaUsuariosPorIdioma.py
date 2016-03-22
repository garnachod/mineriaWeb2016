# -*- coding: utf-8 -*-
import os
import sys
#lib_path = os.path.abspath('/home/dani/github/ConcursoPolicia')
#if lib_path not in sys.path:
#	sys.path.append(lib_path)
import time

import luigi
import json
from DBbridge.ConsultasCassandra import ConsultasCassandra
from ProcesadoresTexto.LimpiadorTweets import LimpiadorTweets
from Config.Conf import Conf
import datetime


class ClasificaUsuariosPorIdioma(luigi.Task):
	"""
	Clasifica los usuarios por el idioma que mas usan en sus ultimos N tweets
	N por defecto es 200

	Returns
	-------
	fichero JSON {idioma: [lista de identificadores de usuario]}
	"""

	"""
		Uso:
			PYTHONPATH='' luigi --module ClasificaUsuariosPorIdioma ClasificaUsuariosPorIdioma
	"""
	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget(path='%s/LuigiTasks/users_idiomas/ClasificaUsuariosPorIdioma/%s/%s/%s.json'%(path, anyo, mes, dia))

	def run(self):
		consultas = ConsultasCassandra()
		usuarios = consultas.getAllUsers()

		dicOld, dicUsers = self.readDicOld()

		for id_twitter, screen_name in usuarios:
			if str(id_twitter) in dicOld:
				continue

			tweets = consultas.getTweetsUsuarioCassandra_lang(id_twitter, limit=200)
			dicIdiomasUser = {}
			for tweet in tweets:
				idioma = tweet.lang
				if idioma not in dicIdiomasUser:
					dicIdiomasUser[idioma] = 0

				dicIdiomasUser[idioma] += 1

			listIdiomasUser = []
			for idioma in dicIdiomasUser:
				listIdiomasUser.append((idioma, dicIdiomasUser[idioma]))

			sortedListIdiomasUser = sorted(listIdiomasUser, key=lambda x: x[1], reverse=True)
			for idioma, contador in sortedListIdiomasUser:
				if idioma != 'und' and contador >= 5:
					if idioma not in dicUsers:
						dicUsers[idioma] =[]

					dicUsers[idioma].append(id_twitter)
					break

		with self.output().open('w') as out_file:
			out_file.write(json.dumps(dicUsers))

	def readDicOld(self, diffDays = 1):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now() - datetime.timedelta(days=diffDays)
		dia = now.day
		mes = now.month
		anyo = now.year

		path = '%s/LuigiTasks/users_idiomas/ClasificaUsuariosPorIdioma/%s/%s/%s.json'%(path, anyo, mes, dia)

		dicUsers_inverse = {}
		dicUsers = {}
		try:
			with open(path, 'r') as in_file:
				dicUsers = json.loads(in_file.read())
				for key in dicUsers:
					for user in dicUsers[key]:
						dicUsers_inverse[str(user)] = key
		except Exception, e:
			print e

		return dicUsers_inverse, dicUsers



class GeneraTextoPorIdioma_topics(luigi.Task):
	"""
	Genera un fichero de usuarios con sus tweets y solo en el idioma determinado
	Topics significa que se pasan stopwords y lematizacion para centrarnos en lo que habla el usuario y no en como habla

	Parameters
	----------
	idioma : idioma de los usuarios que se insertaran en el fichero
	
	Returns
	-------
	Fichero lineas pares identificador de usuario, lineas impares texto en el lenguaje definido
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module ClasificaUsuariosPorIdioma GeneraTextoPorIdioma_topics --idioma
	"""
	idioma = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget(path='%s/LuigiTasks/users_idiomas/GeneraTextoPorIdioma_topics/%s/%s/%s_%s.text'%(path, anyo, mes, dia, self.idioma), 
								format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return ClasificaUsuariosPorIdioma()

	def run(self):
		dicUsers = {}
		with self.input().open('r') as in_file:
			dicUsers = json.loads(in_file.read())

		users_idioma = dicUsers[self.idioma]
		consultas = ConsultasCassandra()
		with self.output().open('w') as out_file:
			for user_id in users_idioma:
				tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(user_id, limit=5000)
				out_file.write(u""+str(user_id))
				out_file.write(u"\n")
				for tweet in tweets:
					if tweet.lang == self.idioma:
						tweetLimpio = LimpiadorTweets.clean(tweet.status)
						tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)
						tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, tweet.lang)
						out_file.write(tweetStemmed)
						out_file.write(u" ")
				out_file.write(u"\n")


class GeneraTextoPorIdioma_semantic(luigi.Task):
	"""
	Genera un fichero de usuarios con sus tweets y solo en el idioma determinado
	semantic significa que no se pasan stopwords ni lematizacion para centrarnos como habla el usuario

	Parameters
	----------
	idioma : idioma de los usuarios que se insertaran en el fichero
	
	Returns
	-------
	Fichero lineas pares identificador de usuario, lineas impares texto en el lenguaje definido
	"""
	idioma = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget(path='%s/LuigiTasks/users_idiomas/GeneraTextoPorIdioma_semantic/%s/%s/%s_%s.text'%(path, anyo, mes, dia, self.idioma), 
								format=luigi.format.TextFormat(encoding='utf8'))
		
	def requires(self):
		return ClasificaUsuariosPorIdioma()

	def run(self):
		dicUsers = {}
		with self.input().open('r') as in_file:
			dicUsers = json.loads(in_file.read())

		users_idioma = dicUsers[self.idioma]
		consultas = ConsultasCassandra()
		with self.output().open('w') as out_file:
			for user_id in users_idioma:
				tweets = consultas.getTweetsUsuarioCassandra_statusAndLang_noRT(user_id, limit=5000)
				out_file.write(u""+str(user_id))
				out_file.write(u"\n")
				for tweet in tweets:
					if tweet.lang == self.idioma:
						tweetLimpio = LimpiadorTweets.clean(tweet.status)
						tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)
						out_file.write(tweetSinStopWords)
						out_file.write(u" ")
				out_file.write(u"\n")
		
class GeneraTextosPorIdiomas(luigi.Task):
	"""
	Genera las tareas de gestion generacion de ficheros de idiomas
	
	Parameters
	----------
	idiomas : string de idiomas en formato (ISO 639-1) separados por ;
	tipo : semantic o topics
	
	Returns
	-------
	Fichero lineas pares identificador de usuario, lineas impares texto en el lenguaje definido
	"""
	tipo = luigi.Parameter(default="topics")
	idiomas = luigi.Parameter(default="ar")

	def requires(self):
		idiomas_split = self.idiomas.split(";")
		tareas = []

		for idioma in idiomas_split:
			if self.tipo == "topics":
				tareas.append(GeneraTextoPorIdioma_topics(idioma))
			else:
				tareas.append(GeneraTextoPorIdioma_semantic(idioma))

		return tareas

	def output(self):
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget(path='users_idiomas/GeneraTextosPorIdiomas/%s/%s/%s.json'%(anyo, mes, dia), 
								format=luigi.format.TextFormat(encoding='utf8'))

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write(u"OK")
	

		

if __name__ == '__main__':
	start_time = time.time()
	ClasificaUsuariosPorIdioma()
	print time.time() - start_time
	#20k users 40.55 segundos