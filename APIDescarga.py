import os

class APIDescarga(object):
	"""
	API para descargar datos desde la interfaz web
	"""
	@staticmethod
	def downloadTwitterUser(username, frecuence=60):
		"""
		Descarga un usuario de twitter,
		 inserta una referencia en la base de datos de descarga, esa referencia se completa al terminar la tarea.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		frecuence : si el usuario ya ha sido descargado hace N minutos antes, no se vuelve a descargar

		Returns
		-------
		identificador de la descarga en segundo plano

		"""

		pass

	@staticmethod
	def downloadTwitterUserRelations(username, frecuence=120):
		"""
		Descarga toda la informacion del circulo Nivel 1 para los posteriores analisis,
		 inserta una referencia en la base de datos de descarga, esa referencia se completa al terminar la tarea.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		frecuence : si el usuario ya ha sido descargado hace N minutos antes, no se vuelve a descargar

		Returns
		-------
		identificador de la descarga en segundo plano

		"""
		pass

	@staticmethod
	def downloadUserMentions(username, frecuence=60):
		"""
		Descarga las menciones de un usuario,
		 inserta una referencia en la base de datos de descarga, esa referencia se completa al terminar la tarea.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		frecuence : si el usuario ya ha sido descargado hace N minutos antes, no se vuelve a descargar

		Returns
		-------
		identificador de la descarga en segundo plano

		"""
		pass

	@staticmethod
	def isDownloadComplete(identificador):
		"""
		Comprueba si una descarga se ha completado

		Parameters
		----------
		identificador : identificador de la descarga

		Returns
		-------
		True si se ha descargado ya, False si no

		"""
		pass