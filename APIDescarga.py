import os
import luigi
from LuigiTasks.RecolectorTwitter import RecolectorUsuarioTwitter

import time

import multiprocessing

class _downloadTwitterUser(multiprocessing.Process):
	"""docstring for ClassName"""
	def __init__(self, username, id_tarea):
		super(_downloadTwitterUser, self).__init__()
		self.username = username
		self.id_tarea = id_tarea
		#self.daemon = True
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/null'

	def run(self):
		f = os.popen("PYTHONPATH='../LuigiTasks' luigi --module RecolectorTwitter RecolectorUsuarioTwitter --usuario " +self.username)
		"""luigi.run(["--usuario", self.username], main_task_cls = RecolectorUsuarioTwitter)"""
		time.sleep(60)

	   
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
			"""p = multiprocessing.Process(target=worker_downloadTwitterUser, args=(username, id_tarea))
			p.daemon = True
			p.start()"""
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
		pass

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