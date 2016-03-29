from DBbridge.ConsultasCassandra import ConsultasCassandra
from Config.Conf import Conf
import luigi

class GenerateSentimentMetions(luigi.Task):
	