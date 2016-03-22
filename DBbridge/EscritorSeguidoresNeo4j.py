from Escritor import Escritor
from Neo4j.ConexionNeo4j import ConexionNeo4j
from py2neo import Node, Relationship, cypher
from ConsultasGeneral import ConsultasGeneral
import time 

class EscritorSeguidoresNeo4j(Escritor):
	"""docstring for EscritorSeguidoresNeo4j"""
	def __init__(self, searchID):
		super(EscritorSeguidoresNeo4j, self).__init__(searchID)
		self.graph = ConexionNeo4j().getGraph()
		self.consultas = ConsultasGeneral()
		self.nodos_creados_historico = {}

		
	def escribe(self, data):
		print len(data)
		nodos_crear = []
		for usuario1, usuario2 in data:
			if str(usuario1) in self.nodos_creados_historico:
				pass
			else:
				nodos_crear.append(usuario1)
				self.nodos_creados_historico[str(usuario1)] = True

			if str(usuario2) in self.nodos_creados_historico:
				pass
			else:
				nodos_crear.append(usuario2)
				self.nodos_creados_historico[str(usuario2)] = True
		
			
		self.write(nodos_crear, data)

	def write(self, nodos_crear, relaciones):
		tx = self.graph.cypher.begin()
		
		for i, nodoCrea in enumerate(nodos_crear):
			query = "MERGE (n:user {id_twitter:" +str(nodoCrea) +"})"
			tx.append(query)
			if i % 100 == 0:
				tx.process()
		tx.process()
		tx.commit()

		#########################
		## Una vez tenemos los nodos se crea el camino si no existe
		#print "usuarios creados"
		
		tx = self.graph.cypher.begin()
		i = 0 
		for usuario1, usuario2 in relaciones:
			query = "MATCH (np:user { id_twitter: "+str(usuario2)+" }),(nf:user { id_twitter: "+str(usuario1)+"}) MERGE (nf)-[r:FOLLOW]->(np) ON CREATE SET r.since = timestamp()" 
			#query = "MATCH (np { id_twitter: "+str(nodo_principal_id)+" }),(nf { id_twitter: "+str(identificador)+"}) CREATE UNIQUE (nf)-[r:FOLLOW {since:"+str(time.time())+"}]->(np)"			
			i += 1
			tx.append(query)
			if i % 100 == 0:
				tx.process()
		tx.process()
		tx.commit()