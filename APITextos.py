from ProcesadoresTexto.GenerateVectorsFromTweets import GenerateVectorsFromTweets
from DBbridge.ConsultasCassandra import ConsultasCassandra
from AnnoyComparators.AnnoyUserVectorSearcher import AnnoyUserVectorSearcher

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
		(por definir)
		"""
		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(username)
		generator = GenerateVectorsFromTweets()
		vector = generator.getVector_topics(tweets, lang)
		searcher = AnnoyUserVectorSearcher()
		return searcher.getSimilarUsers_topics(vector, lang, numberOfSim)

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
		(por definir)

		"""
		pass

	@staticmethod
	def getUsersSimilar_user_all_semantic(username, lang, numberOfSim, id_tarea):
		pass

	@staticmethod
	def getUsersSimilar_user_relations_semantic(username, lang, numberOfSim, id_tarea):
		pass
		
	@staticmethod
	def getUsersSimilar_text_all_topic(text, lang, numberOfSim, id_tarea):
		pass

	@staticmethod
	def getUsersSimilar_text_all_semantic(lext, lang, numberOfSim, id_tarea):
		pass
