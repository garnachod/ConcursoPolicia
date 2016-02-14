

class APITextos(object):
	"""docstring for APITextos"""
	
	@staticmethod
	def getUsersSimilar_user_all_topic(username, lang, numberOfSim):
		"""
		Retorna una lista de usuarios similares a un usuario dado
		 se buscan todos los usuarios conocidos en la base de datos.
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
	def getUsersSimilar_user_relations_topic(username, lang, numberOfSim):
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
	def getUsersSimilar_user_all_semantic(username, lang, numberOfSim):
		pass

	@staticmethod
	def getUsersSimilar_user_relations_semantic(username, lang, numberOfSim):
		pass
		
	@staticmethod
	def getUsersSimilar_text_all_topic(text, lang, numberOfSim):
		pass

	@staticmethod
	def getUsersSimilar_text_all_semantic(lext, lang, numberOfSim):
		pass
