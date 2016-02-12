# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
import re
import json
from blist import blist
from time import time, sleep
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from DBbridge.ConsultasCassandra import ConsultasCassandra

from ProcesadoresTexto.LimpiadorTweets import LimpiadorTweets
from RecolectorTwitter import *
from datetime import date, timedelta, datetime
from dateutil import parser


class GeneradorTextoUsuario(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoUsuario(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def run(self):
		"""
		Realiza una busqueda en la base de datos

		Recolecta los tweets de un usuario dado por nombre de usuario
		o identificador, imprime cada tweet en una linea, han sido limpiados
		"""
		cs = ConsultasCassandra()

		tweets = []
		try:
			tweets = cs.getTweetsUsuarioCassandra(self.usuario, limit=10000)
		except Exception, e:
			pass

		#print len(self.output())
		with self.output().open('w') as out_file:
			for tweet in tweets:
				tweetLimpio = LimpiadorTweets.clean(tweet.status)
				tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)
				tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, tweet.lang)
				out_file.write(tweetStemmed)
				out_file.write(u"\n")


class GeneradorTextoUsuarioSinLem(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoUsuarioSinLem(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def run(self):
		"""
		Realiza una busqueda en la base de datos

		Recolecta los tweets de un usuario dado por nombre de usuario
		o identificador, imprime cada tweet en una linea, han sido limpiados
		"""
		cs = ConsultasCassandra()

		tweets = []
		try:
			tweets = cs.getTweetsUsuarioCassandra(self.usuario, limit=10000)
		except Exception, e:
			pass

		#print len(self.output())
		with self.output().open('w') as out_file:
			for tweet in tweets:
				tweetLimpio = LimpiadorTweets.clean(tweet.status)
				tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)
				out_file.write(tweetSinStopWords)
				out_file.write(u"\n")

class GeneradorTextoPorContenidoSinLem(luigi.Task):
	"""
		Realiza una busqueda en la base de datos

		Recolecta los tweets de un contenido dado e imprime todos los tweets sin /n
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module GeneradorDocumentosTwitter GeneradorTextoPorContenidoSinLem --query ...
	"""
	query = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoPorContenidoSinLem(%s)'%self.query, format=luigi.format.TextFormat(encoding='utf8'))

	def run(self):
		cs = ConsultasCassandra()

		tweets = []
		try:
			tweets = cs.getStatusTopicsCassandra(self.query, limit=10000)
		except Exception, e:
			print e
			pass

		with self.output().open('w') as out_file:
			i = 0
			for tweet in tweets:
				i += 1
				tweetLimpio = LimpiadorTweets.clean(tweet.status)
				tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)
				out_file.write(tweetSinStopWords)
				out_file.write(u"\n")

			print i



class GeneradorTextoSeguidoresUsuario(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module GeneradorDocumentosTwitter GeneradorTextoSeguidoresUsuario --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		"""
			Importante:
				Aquí podemos ver como se genera un fichero utf-8 el Luigi, como son textos, lo necesitamos

		"""
		return luigi.LocalTarget(path='ficheros/GeneradorTextoSeguidoresUsuario(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))
	
	def requires(self):
		consultasNeo4j = ConsultasNeo4j()
		consultasCassandra = ConsultasCassandra()

		# si no es un identificador, se intenta conseguir desde cassandra
		identificador = 0
		try:
			identificador = long(self.usuario)
		except Exception, e:
			if self.usuario[0] == "@":
				self.usuario = self.usuario[1:]
			identificador = consultasCassandra.getUserIDByScreenNameCassandra(self.usuario)

		#solo puede no existir ese identificador si es privado, pero debemos controlarlo
		if identificador > 0:
			seguidores = consultasNeo4j.getListaIDsSeguidoresByUserID(identificador)
			return [GeneradorTextoUsuario(seguidor) for seguidor in seguidores]
		else:
			return []

	def run(self):
		with self.output().open('w') as out_file:
			for input in self.input():
				with input.open('r') as in_file:
					for line in in_file:
						if len(line) > 10:
							out_file.write(line.replace("\n", ""))

					out_file.write(u"\n")

class GeneradorTextoSeguidoresDoc2Vec(luigi.Task):
	"""docstring for GeneradorTextoSeguidoresDoc2Vec"""
	"""
		Uso:
			PYTHONPATH='' luigi --module GeneradorDocumentosTwitter GeneradorTextoSeguidoresDoc2Vec --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoSeguidoresDoc2Vec(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))
			
	def requires(self):
		consultasNeo4j = ConsultasNeo4j()
		consultasCassandra = ConsultasCassandra()

		# si no es un identificador, se intenta conseguir desde cassandra
		identificador = 0
		try:
			identificador = long(self.usuario)
		except Exception, e:
			if self.usuario[0] == "@":
				self.usuario = self.usuario[1:]
			identificador = consultasCassandra.getUserIDByScreenNameCassandra(self.usuario)

		#solo puede no existir ese identificador si es privado, pero debemos controlarlo
		if identificador > 0:
			seguidores = consultasNeo4j.getListaIDsSeguidoresByUserID(identificador)
			tareas = [GeneradorTextoUsuario(seguidor) for seguidor in seguidores]
			tareas.append(GeneradorTextoUsuario(identificador))
			return tareas
		else:
			return []

	def run(self):
		with self.output().open('w') as out_file:
			for input in self.input():
				with input.open('r') as in_file:
					seguidor = input.path.replace("GeneradorTextoUsuario(", "").replace(")", "").replace("ficheros/", "") + u""
					out_file.write(seguidor)
					out_file.write(u"\n")
					for line in in_file:
						if len(line) > 5:
							out_file.write(line.replace("\n", ""))
							out_file.write(u" ")

					out_file.write(u"\n")

class GeneradorTextoSeguidoresDoc2VecResearch(luigi.Task):
	"""docstring for GeneradorTextoSeguidoresDoc2Vec"""
	"""
		Uso:
			PYTHONPATH='' luigi --module GeneradorDocumentosTwitter GeneradorTextoSeguidoresDoc2VecResearch --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoSeguidoresDoc2VecResearch(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))
			
	def requires(self):
		consultasNeo4j = ConsultasNeo4j()
		consultasCassandra = ConsultasCassandra()

		# si no es un identificador, se intenta conseguir desde cassandra
		identificador = 0
		try:
			identificador = long(self.usuario)
		except Exception, e:
			if self.usuario[0] == "@":
				self.usuario = self.usuario[1:]
			identificador = consultasCassandra.getUserIDByScreenNameCassandra(self.usuario)

		#solo puede no existir ese identificador si es privado, pero debemos controlarlo
		if identificador > 0:
			seguidores = consultasNeo4j.getListaIDsSeguidoresByUserID(identificador)
			tareas = [GeneradorTextoUsuarioSinLem(seguidor) for seguidor in seguidores]
			tareas.append(GeneradorTextoUsuarioSinLem(identificador))
			return tareas
		else:
			return []

	def run(self):
		with self.output().open('w') as out_file:
			for input in self.input():
				with input.open('r') as in_file:
					seguidor = input.path.replace("GeneradorTextoUsuarioSinLem(", "").replace(")", "").replace("ficheros/", "") + u""
					out_file.write("user: " + seguidor)
					out_file.write(u"\n")
					for line in in_file:
						if len(line) > 5:
							out_file.write(line)

					out_file.write(u"\n")




class GeneradorTextoCorpusIdioma(luigi.Task):
	"""docstring for GeneradorTextoCorpusIdioma"""
	"""
		Uso:
			PYTHONPATH='' luigi --module GeneradorDocumentosTwitter GeneradorTextoCorpusIdioma --idioma ...
	"""
	idioma = luigi.Parameter(default="es")

	def run(self):
		consultasCassandra = ConsultasCassandra()
		diccionarioUsuarios = {}

		tweets = consultasCassandra.getAllStatusAndIDUserFiltrateLang(self.idioma)
		for tweet in tweets:
			strusuario = str(tweet.tuser)
			
			if strusuario not in diccionarioUsuarios:
				diccionarioUsuarios[strusuario] = []

			tweetLimpio = LimpiadorTweets.clean(tweet.status)
			tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)
			tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, tweet.lang)

			diccionarioUsuarios[strusuario].append(tweetStemmed)

		with self.output().open('w') as out_file:
			for usuario in diccionarioUsuarios:
				for tweet in diccionarioUsuarios[usuario]:
					out_file.write(tweet + u" ")

				out_file.write(u"\n")



	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoCorpusIdioma(%s)'%self.idioma, format=luigi.format.TextFormat(encoding='utf8'))
		
class GeneradorTextoCorpusIdiomaSinLem(luigi.Task):
	"""docstring for GeneradorTextoCorpusIdiomaSinLem"""
	"""
		Uso:
			PYTHONPATH='' luigi --module GeneradorDocumentosTwitter GeneradorTextoCorpusIdiomaSinLem --idioma ...
	"""
	idioma = luigi.Parameter(default="es")

	def run(self):
		consultasCassandra = ConsultasCassandra()
		diccionarioUsuarios = {}

		tweets = consultasCassandra.getAllStatusAndIDUserFiltrateLang(self.idioma)
		for tweet in tweets:
			strusuario = str(tweet.tuser)
			
			if strusuario not in diccionarioUsuarios:
				diccionarioUsuarios[strusuario] = []

			tweetLimpio = LimpiadorTweets.clean(tweet.status)
			tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)

			diccionarioUsuarios[strusuario].append(tweetSinStopWords)

		with self.output().open('w') as out_file:
			for usuario in diccionarioUsuarios:
				for tweet in diccionarioUsuarios[usuario]:
					out_file.write(tweet + u" ")

				out_file.write(u"\n")



	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoCorpusIdiomaSinLem(%s)'%self.idioma, format=luigi.format.TextFormat(encoding='utf8'))
	
if __name__ == "__main__":
	luigi.run()