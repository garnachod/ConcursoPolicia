from APIDescarga import APIDescarga
from DBbridge.ConsultasCassandra import ConsultasCassandra
import re

re_tuser = re.compile(r'^@?[a-zA-Z0-9_]+$')

class APITiempo(object):
	"""docstring for APITextos"""

	@staticmethod
	def getUsersSimilar_user_all(username, lang, numberOfSim, id_tarea):
		"""
		Retorna una lista de usuarios similares a un usuario dado
		 se buscan todos los usuarios conocidos en la base de datos.
		 se busca por mismos temas de conversacion.

		Parameters
		----------
		username : usuario de la red social con @ o sin @
		lang : lenguaje de los usuarios
		numberOfSim : es el numero de usuarios devolver
		id_tarea : identificador de la tarea creada

		Returns
		-------
		lista con la informacion necesaria para la interfaz grafica
		Si ha ocurrido un fallo o no se puede comparar retorna False
		"""
		if id_tarea < 0:
			raise Exception("Parametros incorrectos")

		if len(username) > 16 or len(username) < 2 or re_tuser.match(username) == None:
			raise Exception("Parametros incorrectos")

		if lang != 'es' and lang != 'ar' and lang != 'en' and lang != 'fr':
			raise Exception("Parametros incorrectos")

		if numberOfSim < 1 or numberOfSim > 5000:
			raise Exception("Parametros incorrectos")

		#print id_tarea
		path = APIDescarga.downloadAndGenerateTime(username, lang, id_tarea)
		if path == False:
			return False
		else:
			users = []
			consultas = ConsultasCassandra()
			with open(path, "r") as fin:
				for line in fin:
					users.append(long(line))

			users_long = []
			for user in users:
				user_long = consultas.getUserByIDLargeCassandra_police(user)
				if user_long != False:
					if user_long.screen_name not in username:
						users_long.append(user_long)

				if len(users_long) >= numberOfSim:
					break
			return users_long
	
	@staticmethod
	def getUsersSimilar_user_relations(username, lang, numberOfSim, id_tarea):
		"""
		Retorna una lista de usuarios similares a un usuario dado
		 se buscan todos los usuarios conocidos en la base de datos.
		 se busca por mismos temas de conversacion.

		Parameters
		----------
		username : usuario de la red social con @ o sin @
		lang : lenguaje de los usuarios
		numberOfSim : es el numero de usuarios devolver
		id_tarea : identificador de la tarea creada

		Returns
		-------
		lista con la informacion necesaria para la interfaz grafica
		Si ha ocurrido un fallo o no se puede comparar retorna False
		"""
		if id_tarea < 0:
			raise Exception("Parametros incorrectos")

		if len(username) > 16 or len(username) < 2 or re_tuser.match(username) == None:
			raise Exception("Parametros incorrectos")

		if lang != 'es' and lang != 'ar' and lang != 'en' and lang != 'fr':
			raise Exception("Parametros incorrectos")

		if numberOfSim < 1 or numberOfSim > 5000:
			raise Exception("Parametros incorrectos")

		#print id_tarea
		path = APIDescarga.downloadAndGenerateTimeRelations(username, lang, id_tarea)
		if path == False:
			return False
		else:
			users = []
			consultas = ConsultasCassandra()
			with open(path, "r") as fin:
				for line in fin:
					users.append(long(line))

			users_long = []
			for user in users:
				user_long = consultas.getUserByIDLargeCassandra_police(user)
				if user_long != False:
					if user_long.screen_name not in username:
						users_long.append(user_long)

				if len(users_long) >= numberOfSim:
					break
			return users_long