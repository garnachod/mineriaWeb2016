from RecolectorTweetsUser import RecolectorTweetsUser
from time import time

class RecolectorTweetsTags(RecolectorTweetsUser):
	"""docstring for RecolectorTweetsTags"""
	def __init__(self, escritor):
		super(RecolectorTweetsTags, self).__init__(escritor)
		self.authorizator.set_limit_api(430)
		self.tipo_id = 2
		self.inicializa()
		self.lastQuery = ""
		self.maximo = long(0)
		self.cont = 0


	def recolecta(self, query, limite=20000):
		arrayFinal = []

		if query != self.lastQuery:
			self.maximo = long(0)
			self.cont = 0

		self.lastQuery = query

		while True:
			statuses = self.privateRealizaConsulta(query, maxi=self.maximo)
			if len(statuses) == 0:
				break

			for status in statuses:
				arrayFinal.append(status)
			
			self.maximo = self.getMinIDtweets(arrayFinal, query)
			if self.maximo != 0:
				self.maximo -= 1

			if len(arrayFinal) > 100:
				self.guarda(arrayFinal)
				self.cont += len(arrayFinal)
				arrayFinal = []
				
			#limite puesto por defecto
			if self.cont > limite:
				break

		print self.cont
		
		self.guarda(arrayFinal)

	def privateRealizaConsulta(self, query, maxi=0, mini=0):
		if self.authorizator.is_limit_api(self.tipo_id):
			raise Exception('LIMITE')

		try:
			if maxi == 0 and mini == 0:
				retorno = self.twitter.search(q=query, count='100', result_type="recent")
			elif maxi == 0 and mini > 0:
				retorno = self.twitter.search(q=query, since_id=mini, count='100', result_type="recent")
			elif maxi > 0 and mini == 0:
				retorno = self.twitter.search(q=query, max_id=maxi, count='100', result_type="recent")
			else:
				retorno = self.twitter.search(q=query, max_id=maxi, since_id=mini, count='100', result_type="recent")

			self.authorizator.add_query_to_key(self.tipo_id)
			#print retorno
			return retorno["statuses"]

		except Exception, e:
			print e
			self.authorizator.add_query_to_key(self.tipo_id)
			if "429" in str(e):
				raise Exception('LIMITE')
			return []

