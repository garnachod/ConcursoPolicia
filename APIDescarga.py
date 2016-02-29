import os
import luigi
from LuigiTasks.RecolectorTwitter import RecolectorUsuarioTwitter, RecolectorCirculoUsuario
from DBbridge.ConsultasSQL_police import ConsultasSQL_police
from Config.Conf import Conf

import time

import multiprocessing
import subprocess as sub
from subprocess import PIPE, STDOUT


class _downloadTwitterUser(multiprocessing.Process):
	"""docstring for ClassName"""
	def __init__(self, username, id_tarea):
		super(_downloadTwitterUser, self).__init__()
		self.username = username
		self.id_tarea = id_tarea
		#self.daemon = True

	def run(self):
		#configuracion del sistema
		conf = Conf()
		path = conf.getAbsPath()
		comand = "PYTHONPATH='%s/LuigiTasks' luigi --module RecolectorTwitter RecolectorUsuarioTwitter --usuario " + self.username
		comand += " > /dev/null 2>&1"
		comand = comand%path
		os.popen(comand)
		#p = sub.call(comand, stdout=PIPE,stderr=STDOUT, shell=True)
		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.id_tarea)

class _downloadTwitterRelations(multiprocessing.Process):
	"""docstring for ClassName"""
	def __init__(self, username, id_tarea):
		super(_downloadTwitterRelations, self).__init__()
		self.username = username
		self.id_tarea = id_tarea

	def run(self):
		#configuracion del sistema
		conf = Conf()
		path = conf.getAbsPath()
		comand = "PYTHONPATH='%s/LuigiTasks' luigi --module RecolectorTwitter RecolectorCirculoUsuario --usuario " + self.username
		comand += " > /dev/null 2>&1"
		comand = comand%path
		
		os.popen(comand)
		consultas = ConsultasSQL_police()
		consultas.setFinishedTask(self.id_tarea)
	   
class APIDescarga(object):
	"""
	API para descargar datos desde la interfaz web
	"""
	@staticmethod
	def downloadTwitterUser(username, id_tarea):
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

		recolector = RecolectorUsuarioTwitter(usuario = username)
		if os.path.isfile(recolector.output().path) == False:
			p = _downloadTwitterUser(username, id_tarea)
			p.start()
			print "INICIANDO"
			return False
		else:
			return True


	@staticmethod
	def downloadTwitterUserRelations(username, id_tarea):
		"""
		Descarga toda la informacion del circulo Nivel 1 para los posteriores analisis,
		 inserta una referencia en la base de datos de descarga, esa referencia se completa al terminar la tarea.

		Parameters
		----------
		username : usuario de la red social con @ o sin @ 
		id_tarea : identificador de la tarea para insertar el fin de busqueda

		Returns
		-------
		True si la descarga esta realizada False en caso contrario

		"""
		recolector = RecolectorCirculoUsuario(usuario = username)
		if os.path.isfile(recolector.output().path) == False:
			p = _downloadTwitterRelations(username, id_tarea)
			p.start()
			print "INICIANDO"
			return False
		else:
			return True

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