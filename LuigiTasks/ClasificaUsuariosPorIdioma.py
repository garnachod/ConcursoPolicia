# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import time

import luigi
import json
from DBbridge.ConsultasCassandra import ConsultasCassandra
from ProcesadoresTexto.LimpiadorTweets import LimpiadorTweets


class ClasificaUsuariosPorIdioma(luigi.Task):
	"""
	Clasifica los usuarios por el idioma que mas usan en sus ultimos N tweets
	N por defecto es 200

	Returns
	-------
	fichero JSON {idioma: [lista de identificadores de usuario]}
	"""

	"""
		Uso:
			PYTHONPATH='' luigi --module ClasificaUsuariosPorIdioma ClasificaUsuariosPorIdioma
	"""
	def output(self):
		return luigi.LocalTarget(path='users_idiomas/ClasificaUsuariosPorIdioma(%s)'%time.strftime("%x"))

	def run(self):
		consultas = ConsultasCassandra()
		usuarios = consultas.getAllUsers()

		dicUsers = {}

		for id_twitter, screen_name in usuarios:
			tweets = consultas.getTweetsUsuarioCassandra_lang(id_twitter, limit=200)
			dicIdiomasUser = {}
			for tweet in tweets:
				idioma = tweet.lang
				if idioma not in dicIdiomasUser:
					dicIdiomasUser[idioma] = 0

				dicIdiomasUser[idioma] += 1

			listIdiomasUser = []
			for idioma in dicIdiomasUser:
				listIdiomasUser.append((idioma, dicIdiomasUser[idioma]))

			sortedListIdiomasUser = sorted(listIdiomasUser, key=lambda x: x[1], reverse=True)
			for idioma, contador in sortedListIdiomasUser:
				if idioma != 'und' and contador >= 5:
					if idioma not in dicUsers:
						dicUsers[idioma] =[]

					dicUsers[idioma].append(id_twitter)
					break

		with self.output().open('w') as out_file:
			out_file.write(json.dumps(dicUsers))


class GeneraTextoPorIdioma_topics(luigi.Task):
	"""
	Genera un fichero de usuarios con sus tweets y solo en el idioma determinado
	Topics significa que se pasan stopwords y lematizacion para centrarnos en lo que habla el usuario y no en como habla

	Parameters
	----------
	idioma : idioma de los usuarios que se insertaran en el fichero
	
	Returns
	-------
	Fichero lineas pares identificador de usuario, lineas impares texto en el lenguaje definido
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module ClasificaUsuariosPorIdioma GeneraTextoPorIdioma_topics --idioma
	"""
	idioma = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='users_idiomas/GeneraTextoPorIdioma_topics(%s_%s)'%(self.idioma,time.strftime("%x")), 
								format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return ClasificaUsuariosPorIdioma()

	def run(self):
		dicUsers = {}
		with self.input().open('r') as in_file:
			dicUsers = json.loads(in_file.read())

		users_idioma = dicUsers[self.idioma]
		consultas = ConsultasCassandra()
		with self.output().open('w') as out_file:
			for user_id in users_idioma:
				tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(user_id, limit=5000)
				out_file.write(u""+str(user_id))
				out_file.write(u"\n")
				for tweet in tweets:
					if tweet.lang == self.idioma:
						tweetLimpio = LimpiadorTweets.clean(tweet.status)
						tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)
						tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, tweet.lang)
						out_file.write(tweetStemmed)
						out_file.write(u" ")
				out_file.write(u"\n")


class GeneraTextosPorIdioma_semantic(luigi.Task):
	"""
	Genera un fichero de usuarios con sus tweets y solo en el idioma determinado
	semantic significa que no se pasan stopwords ni lematizacion para centrarnos como habla el usuario

	Parameters
	----------
	idioma : idioma de los usuarios que se insertaran en el fichero
	
	Returns
	-------
	Fichero lineas pares identificador de usuario, lineas impares texto en el lenguaje definido
	"""
	idioma = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='users_idiomas/GeneraTextosPorIdioma_semantic(%s_%s)'%(self.idioma,time.strftime("%x")))
		
	def requires(self):
		return ClasificaUsuariosPorIdioma()
		
class GeneraTextosPorIdiomas(luigi.Task):
	"""
	Genera las tareas de gestion generacion de ficheros de idiomas
	
	Parameters
	----------
	idiomas : string de idiomas en formato (ISO 639-1) separados por ;
	tipo : semantic o topics
	
	Returns
	-------
	Fichero lineas pares identificador de usuario, lineas impares texto en el lenguaje definido
	"""
	tipo = luigi.Parameter(default="topics")
	idiomas = luigi.Parameter(default="ar")

	def requires(self):
		idiomas_split = self.idioma.split(";")
		tareas = []

		for idioma in idiomas_split:
			if tipo == "topics":
				tareas.append(GeneraTextoPorIdioma_topics(idioma))
			else:
				tareas.append(GeneraTextosPorIdioma_semantic(idioma))

		return tareas

	def output(self):
		return luigi.LocalTarget(path='users_idiomas/GeneraTextosPorIdiomas(%s)'%time.strftime("%x"))

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")


	
		

if __name__ == '__main__':
	start_time = time.time()
	ClasificaUsuariosPorIdioma()
	print time.time() - start_time
	#20k users 40.55 segundos