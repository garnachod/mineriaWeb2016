class Escritor(object):
	"""docstring for Escritor"""
	def __init__(self, searchID):
		super(Escritor, self).__init__()
		self.searchID = searchID

	def escribe(self, data):
		raise NotImplementedError( "Should have implemented this" )
		