# -*- coding: utf-8 -*-
import os
import sys
#lib_path = os.path.abspath('/home/dani/github/ConcursoPolicia')
#if lib_path not in sys.path:
#	sys.path.append(lib_path)

import luigi
from ClasificaUsuariosPorIdioma import *
from ProcesadoresTexto.Doc2Vec import Doc2Vec
from annoy import AnnoyIndex

import json
import datetime
from Config.Conf import Conf

class TrainDoc2VecLang_topics(luigi.Task):
	"""
	Genera el modelo de paragraph vector para los textos dado el contenido.
	Dimensiones 50
	Epocas 20
	Metodo DBOW

	Returns
	-------
	fichero .check que solo se usa para comprobar que existe en el resto de tareas.
	fichero .model modelo paragraph vector de la libreria gensim
	"""
	"""
		Uso manual:
			PYTHONPATH='' luigi --module TrainText TrainDoc2VecLang_topics --idioma ar
	"""
	idioma = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		self.path = '%s/LuigiTasks/TrainText/Doc2VecLang_topics/%s/%s/%s_%s.check'%(path,anyo, mes, dia, self.idioma)
		return luigi.LocalTarget(path=self.path)

	def requires(self):
		return GeneraTextoPorIdioma_topics(self.idioma)

	def run(self):
		with self.output().open("w") as out:
			d2v = Doc2Vec()
			savePath = self.path.replace("check","model")
			#print self.input().path
			conf = Conf()
			d2v.train(self.input().path, savePath, dimension = conf.getDimVectors(), epochs = 20, method="DBOW")
			out.write("OK")

class TrainDoc2VecLang_semantic(luigi.Task):
	"""
	Genera el modelo de paragraph vector para los textos dado el contenido y utilizando tambien la forma de hablar.
	Dimensiones 50
	Epocas 20
	Metodo DM

	Returns
	-------
	fichero .check que solo se usa para comprobar que existe en el resto de tareas.
	fichero .model modelo paragraph vector de la libreria gensim
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module TrainText TrainDoc2VecLang_semantic --idioma ar
	"""
	idioma = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		self.path = '%s/LuigiTasks/TrainText/Doc2VecLang_semantic/%s/%s/%s_%s.check'%(path, anyo, mes, dia, self.idioma)
		return luigi.LocalTarget(path=self.path)

	def requires(self):
		return GeneraTextoPorIdioma_semantic(self.idioma)

	def run(self):
		with self.output().open("w") as out:
			d2v = Doc2Vec()
			savePath = self.path.replace("check","model")
			conf = Conf()
			d2v.train(self.input().path, savePath, dimension = conf.getDimVectors(), epochs = 30, method="DM")
			out.write("OK")

class GenerateVecsAnnoyLang_topics(luigi.Task):
	"""
	Genera a partir del modelo de topics computado, vecinos proximos aproximados para que la busqueda
	 de usuarios similares sea mucho mas rapida. https://github.com/spotify/annoy

	Cuidado: el identificador que devuelve annoy no es el mismo que el de twitter,
	 por eso se genera un diccionario JSON que traduce

	Returns
	-------
	fichero .json Diccionario que traduce de indice de usuario twitter a indice annoy
	fichero .annoy modelo en formato annoy
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module TrainText GenerateVecsAnnoyLang_topics --idioma ar
	"""
	idioma = luigi.Parameter()
	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		self.path = '%s/LuigiTasks/AnnoyVecs/topics/%s/%s/%s_%s.json'%(path, anyo, mes, dia, self.idioma)
		return luigi.LocalTarget(path=self.path)

	def requires(self):
		return [GeneraTextoPorIdioma_topics(self.idioma), TrainDoc2VecLang_topics(self.idioma)]

	def run(self):
		text_loc = ""
		ModelLocation = ""
		for input in self.input():
			if "users_idiomas" in input.path:
				text_loc = input.path
			else:
				ModelLocation = input.path.replace("check","model")

		conf = Conf()
		f = conf.getDimVectors()
		t = AnnoyIndex(f)
		d2v = Doc2Vec()
		dic_users_vectos = d2v.simulateVectorsFromUsersFile(text_loc, ModelLocation)
		# diccionario que traduce de id para annoy a id de usuario de twitter
		dic_users_id = {}
		count_users = 0
		for user in dic_users_vectos:
			t.add_item(count_users, dic_users_vectos[user])
			dic_users_id[user] = count_users
			count_users += 1
		#entrenamiento de annoy, 20 arboles para vecinos proximos
		t.build(20)
		with self.output().open("w") as f_out:
			f_out.write(json.dumps(dic_users_id))
			now = datetime.datetime.now()
			dia = now.day
			mes = now.month
			anyo = now.year
			path = self.path
			t.save(path.replace("json","annoy"))

class GenerateVecsAnnoyLang_semantic(luigi.Task):
	"""
	Genera a partir del modelo semantico computado, vecinos proximos aproximados para que la busqueda
	 de usuarios similares sea mucho mas rapida. https://github.com/spotify/annoy

	Cuidado: el identificador que devuelve annoy no es el mismo que el de twitter,
	 por eso se genera un diccionario JSON que traduce

	Returns
	-------
	fichero .json Diccionario que traduce de indice de usuario twitter a indice annoy {"id_usuario":id_annoy}
	fichero .annoy modelo en formato annoy
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module TrainText GenerateVecsAnnoyLang_topics --idioma ar
	"""
	idioma = luigi.Parameter()
	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		self.path = '%s/LuigiTasks/AnnoyVecs/semantic/%s/%s/%s_%s.json'%(path, anyo, mes, dia, self.idioma)
		return luigi.LocalTarget(path=self.path)

	def requires(self):
		return [GeneraTextoPorIdioma_semantic(self.idioma), TrainDoc2VecLang_semantic(self.idioma)]

	def run(self):
		text_loc = ""
		ModelLocation = ""
		for input in self.input():
			if "users_idiomas" in input.path:
				text_loc = input.path
			else:
				ModelLocation = input.path.replace("check","model")

		conf = Conf()
		f = conf.getDimVectors()
		t = AnnoyIndex(f)
		d2v = Doc2Vec()
		dic_users_vectos = d2v.simulateVectorsFromUsersFile(text_loc, ModelLocation)
		# diccionario que traduce de id para annoy a id de usuario de twitter
		dic_users_id = {}
		count_users = 0
		for user in dic_users_vectos:
			t.add_item(count_users, dic_users_vectos[user])
			dic_users_id[user] = count_users
			count_users += 1
		# creacion del 
		t.build(20)
		with self.output().open("w") as f_out:
			f_out.write(json.dumps(dic_users_id))
			now = datetime.datetime.now()
			dia = now.day
			mes = now.month
			anyo = now.year
			path = self.path
			t.save(path.replace("json","annoy"))
		
		