# -*- coding: utf-8 -*-
#Para prueba unitarias
#import os
#import sys
#lib_path = os.path.abspath('/home/dani/tfg/sources')
#sys.path.append(lib_path)

from Cassandra.ConexionCassandra import ConexionCassandra
#from spark.SparkContexto import SparkContexto
from StaticFuncSpark import StaticFuncSpark
from blist import blist
import time


class ConsultasCassandraSpark(object):
	"""docstring for ConsultasCassandraSpark"""
	def __init__(self):
		super(ConsultasCassandraSpark, self).__init__()
		self.session_cassandra = ConexionCassandra().getSession()
		self.sc = None #SparkContexto().getContexto()



	def getAllTweetsNoRtStatusFiltrLangCS(self, lang):
		query = "SELECT status, lang FROM tweets WHERE orig_tweet = 0;"

		try:
			rows = self.session_cassandra.execute(query)
			retorno = blist([])
			for row in rows:
				if row[1] == lang:
					retorno.append(row[0])

			return retorno
			#rows_paralelas = self.sc.parallelize(rows)
			#filtro_lang = lambda x: [x[0]] if lang == x[1] else []
			#return rows_paralelas.flatMap(filtro_lang).collect()
		except Exception, e:
			print "getAllTweetsStatusCassandra"
			print e

	#tupla no_rt, si_rt
	"""
	def getNumTweetsRTCS(self):
		query ="SELECT orig_tweet FROM tweets;"
		try:
			tini = time.time()
			rows = self.session_cassandra.execute(query)
			print "tiempo Cassandra"
			print time.time() - tini
			tini = time.time()
			rows_paralelas = self.sc.parallelize(rows)
			print "tiempo parallelize"
			print time.time() - tini
			filtro_si_rt = lambda x: 1 if x[0] != 0 else 0
			filtro_no_rt = lambda x: 1 if x[0] == 0 else 0
			reduce_f = lambda x, y: x + y
			return rows_paralelas.map(filtro_no_rt).reduce(reduce_f), rows_paralelas.map(filtro_si_rt).reduce(reduce_f)
			
		except Exception, e:
			print str(e)
			return False
	"""
	#tupla no_rt, si_rt
	def getNumTweetsRTCS(self):
		return self.getNumTweetsRTCSDistrib()
		"""query ="SELECT orig_tweet FROM tweets;"
		try:
			rows = self.session_cassandra.execute(query)
			count_no_rt = 0
			count_si_rt = 0
			for row in rows:
				if row[0] == 0:
					count_no_rt += 1
				else:
					count_si_rt += 1
				
			return count_no_rt, count_si_rt

		except Exception, e:
			print str(e)
			return False"""
	#no_media , si_media
	def getNumTweetsMediaCS(self):
		query ="SELECT media_urls FROM tweets WHERE orig_tweet = 0;"
		try:

			rows = self.session_cassandra.execute(query)

			rows_paralelas = self.sc.parallelize(rows)
			filtro_si_media = lambda x: 1 if x[0] is not None else 0
			filtro_no_media = lambda x: 1 if x[0] is None else 0
			reduce_f = lambda x, y: x + y
			return rows_paralelas.map(filtro_no_media).reduce(reduce_f), rows_paralelas.map(filtro_si_media).reduce(reduce_f)
			
		except Exception, e:
			print str(e)
			return False
	#no_media, si_media
	def getAverageRTMediaCS(self):
		query = "SELECT media_urls, retweet_count FROM tweets WHERE orig_tweet = 0;"

		try:
			rows = self.session_cassandra.execute(query)
			rows_paralelas = self.sc.parallelize(rows)
			filtro_si_media = lambda x: x[1] if x[0] is not None else 0
			filtro_no_media = lambda x: x[1] if x[0] is None else 0
			filtro_si_media_total = lambda x: 1 if x[0] is not None else 0
			filtro_no_media_total = lambda x: 1 if x[0] is None else 0
			reduce_f = lambda x, y: x + y

			total_si_media = float(rows_paralelas.map(filtro_si_media_total).reduce(reduce_f))
			total_no_media = float(rows_paralelas.map(filtro_no_media_total).reduce(reduce_f))

			return rows_paralelas.map(filtro_no_media).reduce(reduce_f)/total_no_media, rows_paralelas.map(filtro_si_media).reduce(reduce_f)/total_si_media

		except Exception, e:
			print str(e)
			return False

	#no_media, si_media
	def getAverageRTMediaByIDUserCS(self, user_id):
		query = "SELECT media_urls, retweet_count, orig_tweet FROM tweets WHERE tuser = %s;"

		try:
			rows = self.session_cassandra.execute(query, [user_id])
			rows_paralelas = self.sc.parallelize(rows)
			filtro_si_media = lambda x: x[1] if x[0] is not None and x[2] == 0 else 0
			filtro_no_media = lambda x: x[1] if x[0] is None and x[2] == 0 else 0
			filtro_si_media_total = lambda x: 1 if x[0] is not None and x[2] == 0 else 0
			filtro_no_media_total = lambda x: 1 if x[0] is None and x[2] == 0 else 0
			reduce_f = lambda x, y: x + y

			total_si_media = float(rows_paralelas.map(filtro_si_media_total).reduce(reduce_f))
			total_no_media = float(rows_paralelas.map(filtro_no_media_total).reduce(reduce_f))

			return rows_paralelas.map(filtro_no_media).reduce(reduce_f)/total_no_media, rows_paralelas.map(filtro_si_media).reduce(reduce_f)/total_si_media

		except Exception, e:
			print str(e)
			return False

	def getTweetContainsTextCS(self, text):
		query = "SELECT status FROM tweets WHERE orig_tweet = 0;"

		try:
			rows = self.session_cassandra.execute(query)
			rows_paralelas = self.sc.parallelize(rows)
			filtro_si_text = lambda x: [x[0]] if text in x[0] else []
		
			return rows_paralelas.flatMap(filtro_si_text).collect()
		except Exception, e:
			print str(e)
			return False

	def getTweetContainsTextAndLangCS(self, text, lang):
		query = "SELECT status, id_twitter FROM tweets WHERE lang = %s AND orig_tweet = 0 ALLOW FILTERING;"

		try:
			rows = self.session_cassandra.execute(query, [lang])
			rows_paralelas = self.sc.parallelize(rows)
			filtro_si_text = lambda x: [x[0]] if text in x[0] else []
		
			return rows_paralelas.flatMap(filtro_si_text).collect()
		except Exception, e:
			print str(e)
			return False

	def getNumTweetsRTCSDistrib(self):
		conjuntos = [(0, 635510762140598272), (635510762140598272, 635600238766632960), (635600238766632960, 635684252449828865), (635684252449828865, 635792116199755778), (635792116199755778, 635991646602027008), (635991646602027008, 636080387106574336), (636080387106574336, 0)]
		
		conjuntos_paralelos = self.sc.parallelize(conjuntos)
		array = conjuntos_paralelos.flatMap(StaticFuncSpark.getTweetsAndCount).reduceByKey(lambda x, y: x + y).collect()

		si_rt = 0
		no_rt = 0
		for tupla in array:
			key, value = tupla
			if key == "si_rt":
				si_rt = value
			if key == "no_rt":
				no_rt = value

		return no_rt, si_rt

if __name__ == '__main__':
	ccs = ConsultasCassandraSpark()
	tiempo_inicio = time.time()
	#print ccs.getNumTweetsMediaCS()
	tiempo_fin = time.time()
	print tiempo_fin - tiempo_inicio
	tiempo_inicio = time.time()
	print ccs.getNumTweetsRTCS()
	tiempo_fin = time.time()
	print tiempo_fin - tiempo_inicio
	tiempo_inicio = time.time()
	#print ccs.getAverageRTMediaCS()
	tiempo_fin = time.time()
	print tiempo_fin - tiempo_inicio
	tiempo_inicio = time.time()
	#print ccs.getTweetContainsTextCS(':-(')
	print time.time() - tiempo_inicio
	tiempo_inicio = time.time()
	#print ccs.getNumTweetsRTCSDistrib()
	print time.time() - tiempo_inicio
	#for item in ccs.getTweetContainsText(':-('):
	#	print item
	#time.sleep(200)
	#print ccs.getAllTweetsNoRtStatusFiltrLangCS('es')
	print len(ccs.getTweetContainsTextAndLangCS(':-(', 'es'))
	
	"""
	export SPARK_HOME=/home/dani/spark/spark-1.4.0
	export PATH=$PATH:$SPARK_HOME
	"""