from DBbridge.ConsultasGeneral import ConsultasGeneral

class ApoyoTwitter(object):
	"""docstring for ApoyoTwitter"""
	def __init__(self):
		super(ApoyoTwitter, self).__init__()
		self.consultas = ConsultasGeneral()

	def getLastTweetCollected(self, screen_name=None, identificador=-1):
		if screen_name is not None:
			return self.consultas.getLastTweetCollectedScreenName(screen_name)
		else:
			return self.consultas.getLastTweetCollectedIdentificador(identificador)
		

	def setLastUserTweet(self, maximo, screen_name=None, identificador=-1):
		if screen_name is not None:
			return self.consultas.setLastTweetCollectedScreenName(screen_name, maximo)
		else:
			return self.consultas.setLastTweetCollectedIdentificador(identificador, maximo)

	def getUserIDByScreenName(self, screen_name):
		return self.consultas.getUserIDByScreenName(screen_name)