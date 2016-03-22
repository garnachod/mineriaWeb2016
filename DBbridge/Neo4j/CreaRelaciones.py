from ConexionNeo4j import ConexionNeo4j

if __name__ == '__main__':
	graph = ConexionNeo4j().getGraph()
	graph.schema.create_uniqueness_constraint("user", "id_twitter")
	graph.cypher.execute("CREATE INDEX ON :user(id_twitter)")
	
