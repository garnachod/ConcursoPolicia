from Config.Conf import Conf
from ClasificaUsuariosPorIdioma import *
from RecolectorTwitter import *
from AnnoyComparators.AnnoyModelTime import AnnoyModelTime
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from DBbridge.ConsultasSQL_police import ConsultasSQL_police
from GenerateSim import sendEmail
import luigi
import datetime
import numpy as np

def calculateVector(ts):
	elems = 24 * 7
	vector = np.zeros(elems)
	for t in ts:
		ca = t.created_at
		#print ca.tzinfo
		vector[ca.weekday() * 24 + ca.hour] += 1

	return vector / np.linalg.norm(vector)

class GenerateVecsAnnoyLangTime(luigi.Task):
	"""
	Genera un modelo ANNOY - JSON 

	Returns
	-------
	fichero .json Diccionario que traduce de indice de usuario twitter a indice annoy {"id_usuario":id_annoy}
	fichero .annoy modelo en formato annoy
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module TrainTime GenerateVecsAnnoyLangTime --idioma es
	"""
	idioma = luigi.Parameter()
	def output(self):
		conf = Conf()
		path = conf.getAnnoyTimePath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		self.partial_path = "%s/%s/%s"%(path, anyo, mes)
		self.path = "%s/%s/%s/%s_%s"%(path, anyo, mes, dia, self.idioma)
		return luigi.LocalTarget(path=self.path)

	def requires(self):
		return ClasificaUsuariosPorIdioma()

	def run(self):
		c = ConsultasCassandra()
	
		langs = {}
		with self.input().open("r") as users_json:
			langs = json.loads(users_json.read())
		
		users = []
		for user in langs[self.idioma]:
			ts = c.getOrigTweetAndCreatedAtFromTweetsByUser(user)
			users.append((user, calculateVector(ts)))
			#print user
			
		with self.output().open("w") as fout:
			ann = AnnoyModelTime(self.idioma, self.partial_path)
			ann.train(users)
			fout.write("OK")

class GetSimilarUsers(luigi.Task):
	"""docstring for GetSimilarUsers"""
	idioma = luigi.Parameter()
	usuario = luigi.Parameter()
	idtarea = luigi.IntParameter(default=0)

	def requires(self):
		return RecolectorUsuarioTwitter(self.usuario)

	def output(self):
		conf = Conf()
		path = conf.getAnnoyTimePath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		self.path = "%s/time_global/%s/%s/%s"%(path, anyo, mes, self.usuario)
		return luigi.LocalTarget(path=self.path)

	def getModelLoc(self):
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		#configuracion del sistema
		conf = Conf()
		path = conf.getAnnoyTimePath()

		model_loc = "%s/%s/%s/%s.ann"%(path, anyo, mes, self.idioma)
		months_minus = 1
		while os.path.isfile(model_loc) == False and months_minus < 10:
			now = datetime.datetime.now() - datetime.timedelta(months=months_minus)
			dia = now.day
			mes = now.month
			anyo = now.year

			model_loc = "%s/%s/%s/%s.ann"%(path, anyo, mes, self.idioma)
			months_minus += 1

		if months_minus >= 10:
			raise Exception("modelo no creado")

		return model_loc

	def run(self):
		numberOfSim = 5000
		c = ConsultasCassandra()
		model_loc = self.getModelLoc()

		ann = AnnoyModelTime(self.idioma, model_loc.replace("%s.ann"%self.idioma, ""))
		ts = c.getOrigTweetAndCreatedAtFromTweetsByUser(self.usuario)
		
		users = ann.getSimilar(calculateVector(ts), numberOfSim)
		users_long = []

		for user in users:
			user_long = c.getUserByIDLargeCassandra_police(user)
			if user_long != False:
				if user_long.screen_name not in self.usuario:
					users_long.append(user)

			if len(users_long) >= numberOfSim:
				break

		with self.output().open('w') as out_file:
			for _user in users_long:
				out_file.write(str(_user))
				out_file.write("\n")


		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.idtarea)
		sendEmail(self.idtarea)

class GetSimilarUsersCom(luigi.Task):
	"""docstring for GetSimilarUsersCom"""
	idioma = luigi.Parameter()
	usuario = luigi.Parameter()
	idtarea = luigi.IntParameter(default=0)

	def requires(self):
		return RecolectorCirculoUsuario(self.usuario)

	def output(self):
		conf = Conf()
		path = conf.getAnnoyTimePath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		self.path = "%s/time_comunity/%s/%s/%s"%(path, anyo, mes, self.usuario)
		return luigi.LocalTarget(path=self.path)

	def run(self):
		c = ConsultasCassandra()
		ts = c.getOrigTweetAndCreatedAtFromTweetsByUser(self.usuario)
		vector = calculateVector(ts)
		#se generan los vectores de todos los usuarios
		consultasNeo4j = ConsultasNeo4j()
		userID = c.getUserIDByScreenNameCassandra(self.usuario)
		seguidoresysiguiendo = consultasNeo4j.getSiguiendoOrSeguidosByUserID(userID)
		relaciones_coseno = []
		for user in seguidoresysiguiendo:
			ts_ = c.getOrigTweetAndCreatedAtFromTweetsByUser(user)
			vector_ = np.array([calculateVector(ts_)]).T
			coseno = np.dot(vector, vector_)[0]
			relaciones_coseno.append((user, coseno))

		relaciones_coseno = sorted(relaciones_coseno, key=lambda x: x[1], reverse=True)

		with self.output().open('w') as out_file:
			for relacion in relaciones_coseno:
				out_file.write(str(relacion[0]))
				out_file.write("\n")

		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.idtarea)
		sendEmail(self.idtarea)


