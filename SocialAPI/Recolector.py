class Recolector(object):
	"""docstring for Recolector"""
	def __init__(self, escritores):
		super(Recolector, self).__init__()
		self.escritores = escritores

	def inicializa(self):
		raise NotImplementedError( "Should have implemented this" )

	def recolecta(self, query):
		raise NotImplementedError( "Should have implemented this" )

	def guarda(self, arrayDatos):
		raise NotImplementedError( "Should have implemented this" )
		