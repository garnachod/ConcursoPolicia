import os
import luigi
from LuigiTasks.RecolectorTwitter import RecolectorUsuarioTwitter, RecolectorCirculoUsuario
from LuigiTasks.GenerateSim import GenerateSimRelations_semantic, GenerateSimRelations_topics, GenerateSimAll_topics, GenerateSimAll_semantic
from LuigiTasks.TrainTime import GetSimilarUsers, GetSimilarUsersCom
from DBbridge.ConsultasSQL_police import ConsultasSQL_police

from Config.Conf import Conf

import time

import multiprocessing


class _generateTwitterUser(multiprocessing.Process):
	"""docstring for _generateTwitterUser"""
	def __init__(self, username, lang, semantic, id_tarea):
		super(_generateTwitterUser, self).__init__()
		self.username = username
		self.lang = lang
		self.semantic = semantic
		self.id_tarea = id_tarea

	def run(self):
		#configuracion del sistema
		conf = Conf()
		path = conf.getAbsPath()
		venv = conf.getVenvPath()
		if venv == "":
			comand = "luigi --module LuigiTasks.GenerateSim " 
		else:
			comand = venv + "/bin/luigi --module LuigiTasks.GenerateSim " 
		if self.semantic == True:
			comand += "GenerateSimAll_semantic "
		else:
			comand += "GenerateSimAll_topics "
		comand += "--usuario " + self.username + " --lang " + self.lang + "  --idtarea " + str(self.id_tarea)
		comand += " > /dev/null 2>&1"

		os.popen(comand)

class _generateTwitterRelations(multiprocessing.Process):
	def __init__(self, username, lang, semantic, id_tarea):
		super(_generateTwitterRelations, self).__init__()
		self.username = username
		self.lang = lang
		self.semantic = semantic
		self.id_tarea = id_tarea

	def run(self):
		#configuracion del sistema
		conf = Conf()
		path = conf.getAbsPath()
		venv = conf.getVenvPath()
		if venv == "":
			comand = "luigi --module LuigiTasks.GenerateSim "
		else:
			comand = venv + "/bin/luigi --module LuigiTasks.GenerateSim "
		if self.semantic == True:
			comand += "GenerateSimRelations_semantic "
		else:
			comand += "GenerateSimRelations_topics "
		comand += "--usuario " + self.username + " --lang " + self.lang + "  --idtarea " + str(self.id_tarea)
		comand += " > /dev/null 2>&1"
		
		os.popen(comand)

class _generateTwitterTime(multiprocessing.Process):
	"""docstring for GenerateTwitterTime"""
	def __init__(self, username, lang, id_tarea):
		super(_generateTwitterTime, self).__init__()
		self.username = username
		self.lang = lang
		self.id_tarea = id_tarea

	def run(self):
		#configuracion del sistema
		conf = Conf()
		path = conf.getAbsPath()
		venv = conf.getVenvPath()
		if venv == "":
			comand = "luigi --module LuigiTasks.TrainTime GetSimilarUsers "
		else:
			comand = venv + "/bin/luigi --module LuigiTasks.TrainTime GetSimilarUsers "
		comand += "--usuario " + self.username + " --idioma " + self.lang + "  --idtarea " + str(self.id_tarea)
		#comand += " > /dev/null 2>&1"
		
		salida = os.popen(comand)
		print salida

class _generateTwitterTimeCom(multiprocessing.Process):
	"""docstring for GenerateTwitterTime"""
	def __init__(self, username, lang, id_tarea):
		super(_generateTwitterTime, self).__init__()
		self.username = username
		self.lang = lang
		self.id_tarea = id_tarea

	def run(self):
		#configuracion del sistema
		conf = Conf()
		path = conf.getAbsPath()
		venv = conf.getVenvPath()
		if venv == "":
			comand = "luigi --module LuigiTasks.TrainTime GetSimilarUsersCom "
		else:
			comand = venv + "/bin/luigi --module LuigiTasks.TrainTime GetSimilarUsersCom "
		comand += "--usuario " + self.username + " --idioma " + self.lang + "  --idtarea " + str(self.id_tarea)
		#comand += " > /dev/null 2>&1"
		
		salida = os.popen(comand)
		print salida
		
		
 	   
class APIDescarga(object):
	"""
	API para descargar datos desde la interfaz web
	"""
	@staticmethod
	def downloadTwitterUser(username, lang, semantic, id_tarea):
		"""
		Descarga un usuario de twitter,
		 inserta una referencia en la base de datos de descarga, esa referencia se completa al terminar la tarea.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		id_tarea : identificador de la tarea para insertar el fin de busqueda

		Returns
		-------
		True si la descarga esta realizada False en caso contrario
		"""
		recolector = None
		if semantic == True:
			recolector = GenerateSimAll_semantic(usuario = username, lang = lang, idtarea=id_tarea)
		else:
			recolector = GenerateSimAll_topics(usuario = username, lang = lang, idtarea=id_tarea)

		if os.path.isfile(recolector.output().path) == False:
			p = _generateTwitterUser(username, lang, semantic, id_tarea)
			p.start()
			return False
		else:
			consultas = ConsultasSQL_police()
			consultas.setFinishedTask(id_tarea)
			return recolector.output().path


	@staticmethod
	def downloadTwitterUserRelations(username, lang, semantic, id_tarea):
		"""
		Descarga toda la informacion del circulo Nivel 1 para los posteriores analisis,
		 inserta una referencia en la base de datos de descarga, esa referencia se completa al terminar la tarea.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		id_tarea : identificador de la tarea para insertar el fin de busqueda

		Returns
		-------
		ruta de las relaciones si la descarga esta realizada False en caso contrario

		"""
		recolector = None
		if semantic == True:
			recolector = GenerateSimRelations_semantic(usuario = username, lang = lang, idtarea=id_tarea)
		else:
			recolector = GenerateSimRelations_topics(usuario = username, lang = lang, idtarea=id_tarea)

		if os.path.isfile(recolector.output().path) == False:
			p = _generateTwitterRelations(username, lang, semantic, id_tarea)
			p.start()
			return False
		else:
			consultas = ConsultasSQL_police()
			consultas.setFinishedTask(id_tarea)
			return recolector.output().path

	@staticmethod
	def downloadAndGenerateTime(username, lang, id_tarea):
		"""
		Descarga un usuario de twitter,
		 inserta una referencia en la base de datos de descarga, esa referencia se completa al terminar la tarea.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		id_tarea : identificador de la tarea para insertar el fin de busqueda

		Returns
		-------
		True si la descarga esta realizada False en caso contrario
		"""
		recolector = None
		#recolector = CLASS
		recolector = GetSimilarUsers(usuario = username, idioma = lang, idtarea=id_tarea)
		if os.path.isfile(recolector.output().path) == False:
			p = _generateTwitterTime(username, lang, id_tarea)
			p.start()
			return False
		else:
			consultas = ConsultasSQL_police()
			consultas.setFinishedTask(id_tarea)
			return recolector.output().path

	@staticmethod
	def downloadAndGenerateTimeRelations(username, lang, id_tarea):
		"""
		Descarga un usuario de twitter,
		 inserta una referencia en la base de datos de descarga, esa referencia se completa al terminar la tarea.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		id_tarea : identificador de la tarea para insertar el fin de busqueda

		Returns
		-------
		True si la descarga esta realizada False en caso contrario
		"""
		recolector = None
		#recolector = CLASS
		recolector = GetSimilarUsersCom(usuario = username, idioma = lang, idtarea=id_tarea)
		if os.path.isfile(recolector.output().path) == False:
			p = _generateTwitterTimeCom(username, lang, id_tarea)
			p.start()
			return False
		else:
			consultas = ConsultasSQL_police()
			consultas.setFinishedTask(id_tarea)
			return recolector.output().path

	@staticmethod
	def downloadUserMentions(username, id_tarea):
		"""
		Descarga las menciones de un usuario,
		 inserta una referencia en la base de datos de descarga, esa referencia se completa al terminar la tarea.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		id_tarea : identificador de la tarea para insertar el fin de busqueda

		Returns
		-------
		True si la descarga esta realizada False en caso contrario

		"""
		pass