from Escritor import Escritor
from Neo4j.ConexionNeo4j import ConexionNeo4j
from py2neo import cypher
from ConsultasGeneral import ConsultasGeneral


class EscritorFavoritosNeo4j(Escritor):
	"""docstring for EscritorFavoritosNeo4j"""
	def __init__(self, searchID):
		super(EscritorFavoritosNeo4j, self).__init__(searchID)
		self.graph = ConexionNeo4j().getGraph()
		self.consultas = ConsultasGeneral()
		self.usuarios_creados_historico = {}
		self.tweets_creados_historico = {}

		
	def escribe(self, data):
		usuarios_crear = []
		tweets_crear = []
		for usuario, tweet_id in data:
			if str(usuario) in self.usuarios_creados_historico:
				pass
			else:
				usuarios_crear.append(usuario)
				self.usuarios_creados_historico[str(usuario)] = True

			if str(tweet_id) in self.tweets_creados_historico:
				pass
			else:
				tweets_crear.append(tweet_id)
				self.tweets_creados_historico[str(tweet_id)] = True
		
			
		self.write(usuarios_crear, tweets_crear, data)

	def write(self, nodos_crear, tweets_crear, relaciones):
		tx = self.graph.cypher.begin()
		
		for i, nodoCrea in enumerate(nodos_crear):
			query = "MERGE (n:user {id_twitter:" +str(nodoCrea) +"})"
			tx.append(query)
			if i % 100 == 0:
				tx.process()
		tx.process()
		tx.commit()

		tx = self.graph.cypher.begin()
		for i, nodoCrea in enumerate(tweets_crear):
			query = "MERGE (n:tweet {id_twitter:" +str(nodoCrea) +"})"
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
		for usuario1, tweet_id in relaciones:
			query = "MATCH (np:user { id_twitter: "+str(usuario1)+" }),(tw:tweet { id_twitter: "+str(tweet_id)+"}) MERGE (np)-[r:FAV]->(tw) ON CREATE SET r.since = timestamp()" 
			#query = "MATCH (np { id_twitter: "+str(nodo_principal_id)+" }),(nf { id_twitter: "+str(identificador)+"}) CREATE UNIQUE (nf)-[r:FOLLOW {since:"+str(time.time())+"}]->(np)"			
			i += 1
			tx.append(query)
			if i % 50 == 0:
				tx.process()
		tx.process()
		tx.commit()