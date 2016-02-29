from ProcesadoresTexto.GenerateVectorsFromTweets import GenerateVectorsFromTweets
from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from AnnoyComparators.AnnoyUserVectorSearcher import AnnoyUserVectorSearcher
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from APIDescarga import APIDescarga
from collections import namedtuple
import numpy as np

class APITextos(object):
	"""docstring for APITextos"""
	
	@staticmethod
	def getUsersSimilar_user_all_topic(username, lang, numberOfSim, id_tarea):
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
		if APIDescarga.downloadTwitterUser(username, id_tarea) == True:
			consultas = ConsultasCassandra()
			tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(username)
			generator = GenerateVectorsFromTweets()
			vector = generator.getVector_topics(tweets, lang)
			searcher = AnnoyUserVectorSearcher()
			users = searcher.getSimilarUsers_topics(vector, lang, numberOfSim + 1)
			users_long = []
			for user in users:
				user_long = consultas.getUserByIDLargeCassandra_police(user)
				if user_long != False:
					if user_long.screen_name not in username:
						users_long.append(user_long)

				if len(users_long) >= numberOfSim:
					break
			return users_long
		else:
			return False

	@staticmethod
	def getUsersSimilar_user_relations_topic(username, lang, numberOfSim, id_tarea):
		"""
		Retorna una lista de usuarios similares a un usuario dado
		 se buscan solo entre sus seguidores y siguendo.
		 se busca por mismos temas de conversacion.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		lang : lenguaje de los usuarios
		numberOfSim : es el numero de usuarios devolver

		Returns
		-------
		lista con la informacion necesaria para la interfaz grafica

		"""
		if APIDescarga.downloadTwitterUserRelations(username, id_tarea) == True:
			consultas = ConsultasCassandra()
			tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(username)
			generator = GenerateVectorsFromTweets()
			vector = generator.getVector_topics(tweets, lang)
			#se generan los vectores de todos los usuarios
			consultasNeo4j = ConsultasNeo4j()
			userID = consultas.getUserIDByScreenNameCassandra(username)
			seguidoresysiguiendo = consultasNeo4j.getSiguiendoOrSeguidosByUserID(userID)
			relaciones_coseno = []
			for user in seguidoresysiguiendo:
				tweets_ = consultas.getTweetsUsuarioCassandra_statusAndLang(user)
				vector_ = np.array([generator.getVector_topics(tweets, lang)]).T
				coseno = np.dot(vector, vector_)[0]
				relaciones_coseno.append((user, coseno))

			relaciones_coseno = sorted(relaciones_coseno, key=lambda x: x[1], reverse=True)

			users_long = []
			length = min(len(relaciones_coseno), numberOfSim)
			for i in xrange(length):
				user_long = consultas.getUserByIDLargeCassandra_police(relaciones_coseno[i][0])
				if user_long != False:
					users_long.append(user_long)

			return users_long
		else:
			return False

	@staticmethod
	def getUsersSimilar_user_all_semantic(username, lang, numberOfSim, id_tarea):
		"""
		Retorna una lista de usuarios similares a un usuario dado
		 se buscan todos los usuarios conocidos en la base de datos.
		 se busca por semantica.

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
		if APIDescarga.downloadTwitterUser(username, id_tarea) == True:
			consultas = ConsultasCassandra()
			tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(username)
			generator = GenerateVectorsFromTweets()
			vector = generator.getVector_semantic(tweets, lang)
			searcher = AnnoyUserVectorSearcher()
			users = searcher.getSimilarUsers_semantic(vector, lang, numberOfSim + 1)
			users_long = []
			for user in users:
				user_long = consultas.getUserByIDLargeCassandra_police(user)
				if user_long != False:
					if user_long.screen_name not in username:
						users_long.append(user_long)

				if len(users_long) >= numberOfSim:
					break
			return users_long
		else:
			return False

	@staticmethod
	def getUsersSimilar_user_relations_semantic(username, lang, numberOfSim, id_tarea):
		"""
		Retorna una lista de usuarios similares a un usuario dado
		 se buscan solo entre sus seguidores y siguendo.
		 se busca por semantica.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		lang : lenguaje de los usuarios
		numberOfSim : es el numero de usuarios devolver
		id_tarea : identificador de la tarea creada

		Returns
		-------
		lista con la informacion necesaria para la interfaz grafica

		"""
		if APIDescarga.downloadTwitterUserRelations(username, id_tarea) == True:
			consultas = ConsultasCassandra()
			tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(username)
			generator = GenerateVectorsFromTweets()
			vector = generator.getVector_semantic(tweets, lang)
			#se generan los vectores de todos los usuarios
			consultasNeo4j = ConsultasNeo4j()
			userID = consultas.getUserIDByScreenNameCassandra(username)
			seguidoresysiguiendo = consultasNeo4j.getSiguiendoOrSeguidosByUserID(userID)
			relaciones_coseno = []
			for user in seguidoresysiguiendo:
				tweets_ = consultas.getTweetsUsuarioCassandra_statusAndLang(user)
				vector_ = np.array([generator.getVector_semantic(tweets, lang)]).T
				coseno = np.dot(vector, vector_)[0]
				relaciones_coseno.append((user, coseno))

			relaciones_coseno = sorted(relaciones_coseno, key=lambda x: x[1], reverse=True)

			users_long = []
			length = min(len(relaciones_coseno), numberOfSim)
			for i in xrange(length):
				user_long = consultas.getUserByIDLargeCassandra_police(relaciones_coseno[i][0])
				if user_long != False:
					users_long.append(user_long)

			return users_long
		else:
			return False
		
	@staticmethod
	def getUsersSimilar_text_all_topic(text, lang, numberOfSim, id_tarea):
		"""
		Retorna una lista de usuarios similares a un texto dado
		 se buscan todos los usuarios conocidos en la base de datos.
		 se busca por temas.

		Parameters
		----------
		texto : texto a comparar
		lang : lenguaje de los usuarios
		numberOfSim : es el numero de usuarios devolver
		id_tarea : identificador de la tarea creada

		Returns
		-------
		lista con la informacion necesaria para la interfaz grafica
		Si ha ocurrido un fallo o no se puede comparar retorna False
		"""
		Row = namedtuple('Row', 'status, lang')
		tweets = [Row(text, lang)]
		generator = GenerateVectorsFromTweets()
		vector = generator.getVector_topics(tweets, lang)
		searcher = AnnoyUserVectorSearcher()
		users = searcher.getSimilarUsers_topics(vector, lang, numberOfSim + 1)
		users_long = []
		for user in users:
			user_long = consultas.getUserByIDLargeCassandra_police(user)
			if user_long != False:
				users_long.append(user_long)

			if len(users_long) >= numberOfSim:
				break

		return users_long
		

	@staticmethod
	def getUsersSimilar_text_all_semantic(text, lang, numberOfSim, id_tarea):
		"""
		Retorna una lista de usuarios similares a un texto dado
		 se buscan todos los usuarios conocidos en la base de datos.
		 se busca por semantica.

		Parameters
		----------
		texto : texto a comparar
		lang : lenguaje de los usuarios
		numberOfSim : es el numero de usuarios devolver
		id_tarea : identificador de la tarea creada

		Returns
		-------
		lista con la informacion necesaria para la interfaz grafica
		Si ha ocurrido un fallo o no se puede comparar retorna False
		"""
		Row = namedtuple('Row', 'status, lang')
		tweets = [Row(text, lang)]
		generator = GenerateVectorsFromTweets()
		vector = generator.getVector_semantic(tweets, lang)
		searcher = AnnoyUserVectorSearcher()
		users = searcher.getSimilarUsers_semantic(vector, lang, numberOfSim)
		users_long = []
		for user in users:
			user_long = consultas.getUserByIDLargeCassandra_police(user)
			if user_long != False:
				users_long.append(user_long)

		return users_long
