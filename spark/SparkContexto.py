# -*- coding: utf-8 -*-
import os
import sys
from Config.Conf import Conf
lib_path = os.path.abspath(Conf().getSparkHome() + '/python')
sys.path.append(lib_path)
from pyspark import SparkConf, SparkContext


class SparkContexto():
	"""docstring for SparkContexto"""
	class __impl:
		"""docstring for __impl"""
		def __init__(self):
			self.conf = (SparkConf()
			 .setMaster("local[8]")
			 .setAppName("My app")
			 .set("spark.executor.memory", "6g")
			 .set("spark.driver.memory", "4g")
			 .setSparkHome(Conf().getSparkHome()))
			self.sc = SparkContext(conf = self.conf)
			
		def getContexto(self):
			return self.sc
			#return None


	# storage for the instance reference
	__instance = None

	def __init__(self):
		if SparkContexto.__instance is None:
			SparkContexto.__instance = SparkContexto.__impl()

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)
			


