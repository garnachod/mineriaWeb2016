# -*- coding: utf-8 -*-
#import os
#import sys
#lib_path = os.path.abspath('../')
#sys.path.append(lib_path)

from Neo4j.ConexionNeo4j import ConexionNeo4j
from blist import blist
from py2neo import cypher

class ConsultasNeo4j(object):
	"""docstring for ConsultasNeo4j"""
	def __init__(self):
		super(ConsultasNeo4j, self).__init__()
		self.graph = ConexionNeo4j().getGraph()

	def getListaIDsSeguidoresByUserID(self, user_id):
		queryNeo4j = "MATCH (a)-[r:FOLLOW]->(u:user {id_twitter : {ID}}) return a"
		nodos = self.graph.cypher.execute(queryNeo4j, {"ID":user_id})
		identificadores = blist([])
		for nodo in nodos:
			identificadores.append(long(nodo[0].properties["id_twitter"]))

		return identificadores

	def getListaIDsSiguiendoByUserID(self, user_id):
		queryNeo4j = "MATCH (u:user {id_twitter : {ID}})-[r:FOLLOW]->(a) return a"
		nodos = self.graph.cypher.execute(queryNeo4j, {"ID":user_id})
		identificadores = blist([])
		for nodo in nodos:
			identificadores.append(long(nodo[0].properties["id_twitter"]))

		return identificadores

	def getSiguiendoOrSeguidosByUserID(self, user_id):
		seguidores = self.getListaIDsSeguidoresByUserID(user_id)
		seguidores_dic = {}
		for seguidor in seguidores_dic:
			seguidores_dic[str(seguidor)] = True

		siguiendo = self.getListaIDsSiguiendoByUserID(user_id)
		for siguiendo_u in siguiendo:
			if str(siguiendo_u) not in seguidores_dic:
				seguidores_dic[str(siguiendo_u)] = True

		retornoList = []
		for key in seguidores_dic:
			retornoList.append(long(key))

		return retornoList

	def getListaIDsFavsByUserID(self, user_id):
		queryNeo4j = "MATCH (u:user {id_twitter : {ID}})-[r:FAV]->(a:tweet) return a"
		nodos = self.graph.cypher.execute(queryNeo4j, {"ID":user_id})
		identificadores = blist([])
		for nodo in nodos:
			identificadores.append(long(nodo[0].properties["id_twitter"]))

		return identificadores

	def getUsersFavTweetByID(self, tweet_id):
		queryNeo4j = "MATCH (u:user)-[r:FAV]->(a:tweet  {id_twitter : {ID}}) return u"
		nodos = self.graph.cypher.execute(queryNeo4j, {"ID":tweet_id})
		identificadores = blist([])
		for nodo in nodos:
			identificadores.append(long(nodo[0].properties["id_twitter"]))

		return identificadores

	def getNumberOfUsers(self):
		queryNeo4j = "MATCH (u:user) return count(*)"
		nodos = self.graph.cypher.execute(queryNeo4j)
		print nodos

if __name__ == '__main__':
	consultas = ConsultasNeo4j()
	#funcionando
	#print consultas.getListaIDsSeguidoresByUserID(2383366169)
	consultas.getNumberOfUsers()
