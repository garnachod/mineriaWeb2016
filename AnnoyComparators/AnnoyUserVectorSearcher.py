import os.path
from annoy import AnnoyIndex
import json
import datetime
from Config.Conf import Conf

class AnnoyUserVectorSearcher(object):
	"""docstring for AnnoyUserVectorSearcher"""
	def __init__(self):
		super(AnnoyUserVectorSearcher, self).__init__()

	def getSimilarUsers_topics(self,vector, lang, numberSim):
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		#configuracion del sistema
		conf = Conf()
		path = conf.getAbsPath()
		
		json_loc = '%s/LuigiTasks/AnnoyVecs/topics/%s/%s/%s_%s.json'%(path, anyo, mes, dia, lang)
		model_loc = '%s/LuigiTasks/AnnoyVecs/topics/%s/%s/%s_%s.annoy'%(path, anyo, mes, dia, lang)
		days_minus = 1
		while os.path.isfile(model_loc) == False and days_minus < 20:
			now = datetime.datetime.now() - datetime.timedelta(days=days_minus)
			dia = now.day
			mes = now.month
			anyo = now.year

			json_loc = '%s/LuigiTasks/AnnoyVecs/topics/%s/%s/%s_%s.json'%(path, anyo, mes, dia, lang)
			model_loc = '%s/LuigiTasks/AnnoyVecs/topics/%s/%s/%s_%s.annoy'%(path, anyo, mes, dia, lang)
			days_minus += 1

		dicInverse = {}
		with open(json_loc, "r") as json_fin:
			dic = json.loads(json_fin.read())
			for key in dic:
				dicInverse[str(dic[key])] = long(key)
		
		u = AnnoyIndex(conf.getDimVectors())
		u.load(model_loc)

		similarElem, values = u.get_nns_by_vector(vector, 100000, include_distances=True)
		best = []
		
		for i in xrange(numberSim):
			best.append(dicInverse[str(similarElem[i])])

		return best

	def getSimilarUsers_semantic(self,vector, lang, numberSim):
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		#configuracion del sistema
		conf = Conf()
		path = conf.getAbsPath()
		
		json_loc = '%s/LuigiTasks/AnnoyVecs/semantic/%s/%s/%s_%s.json'%(path, anyo, mes, dia, lang)
		model_loc = '%s/LuigiTasks/AnnoyVecs/semantic/%s/%s/%s_%s.annoy'%(path, anyo, mes, dia, lang)
		days_minus = 1
		while os.path.isfile(model_loc) == False and days_minus < 20:
			now = datetime.datetime.now() - datetime.timedelta(days=days_minus)
			dia = now.day
			mes = now.month
			anyo = now.year

			json_loc = '%s/LuigiTasks/AnnoyVecs/semantic/%s/%s/%s_%s.json'%(path, anyo, mes, dia, lang)
			model_loc = '%s/LuigiTasks/AnnoyVecs/semantic/%s/%s/%s_%s.annoy'%(path, anyo, mes, dia, lang)
			days_minus += 1

		dicInverse = {}
		with open(json_loc, "r") as json_fin:
			dic = json.loads(json_fin.read())
			for key in dic:
				dicInverse[str(dic[key])] = long(key)
		
		u = AnnoyIndex(conf.getDimVectors())
		u.load(model_loc)

		similarElem, values = u.get_nns_by_vector(vector, 100000, include_distances=True)
		best = []
		
		for i in xrange(numberSim):
			best.append(dicInverse[str(similarElem[i])])

		return best



if __name__ == '__main__':
	vector = [-0.33329046, -0.06020588, -0.10107401, 0.16904078, 0.03298073, -0.39123034 , 0.07169889, -0.25156903, -0.03312016, -0.22661768, 0.73603529, -0.00803526 , -0.09268218, -0.05567983, 0.06042934, 0.0305442, -0.08666425, 0.15310751, 0.32358646, 0.17965902, -0.51564187, 0.0182211, -0.14344144, 0.23940711 , 0.22054118, -0.05098, -0.00219033, -0.21284446, -0.03327479, -0.08236339, -0.04903975, -0.40647417, -0.24776892, 0.15795128, 0.1893689, 0.52428573, 0.11683933, -0.60566133, 0.40511072, -0.15539889, 0.16456138, 0.22143982, 0.19832087, 0.21323819, 0.10884467, -0.11417814, -0.13561803, 0.31303912, -0.24594554, -0.00476049]
	print AnnoyUserVectorSearcher().getSimilarUsers_topics(vector, "ar", 100)