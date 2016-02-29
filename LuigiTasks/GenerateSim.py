# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import luigi
from RecolectorTwitter import *
from Config.Conf import Conf
from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from ProcesadoresTexto.GenerateVectorsFromTweets import GenerateVectorsFromTweets
import datetime
import numpy as np

class GenerateSimRelations_semantic(luigi.Task):
	usuario = luigi.Parameter()
	lang = luigi.Parameter()

	def requires(self):
		return RecolectorCirculoUsuario(self.usuario)

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget('%s/LuigiTasks/similitudes/semantic/%s/%s/%s_%s_%s'%(path, anyo, mes, self.usuario, self.lang))

	def run(self):
		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(self.usuario)
		generator = GenerateVectorsFromTweets()
		vector = generator.getVector_semantic(tweets, self.lang)
		#se generan los vectores de todos los usuarios
		consultasNeo4j = ConsultasNeo4j()
		userID = consultas.getUserIDByScreenNameCassandra(self.usuario)
		seguidoresysiguiendo = consultasNeo4j.getSiguiendoOrSeguidosByUserID(userID)
		relaciones_coseno = []
		for user in seguidoresysiguiendo:
			tweets_ = consultas.getTweetsUsuarioCassandra_statusAndLang(user)
			vector_ = np.array([generator.getVector_semantic(tweets, self.lang)]).T
			coseno = np.dot(vector, vector_)[0]
			relaciones_coseno.append((user, coseno))

		relaciones_coseno = sorted(relaciones_coseno, key=lambda x: x[1], reverse=True)

		with self.output().open('w') as out_file:
			for relacion in relaciones_coseno:
				out_file.write(str(relacion[0]))
				out_file.write("\n")

class GenerateSimRelations_topics(luigi.Task):
	usuario = luigi.Parameter()
	lang = luigi.Parameter()

	def requires(self):
		return RecolectorCirculoUsuario(self.usuario)

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget('%s/LuigiTasks/similitudes/topic/%s/%s/%s_%s'%(path, anyo, mes, self.usuario, self.lang))

	def run(self):
		consultas = ConsultasCassandra()
		tweets = consultas.getTweetsUsuarioCassandra_statusAndLang(self.usuario)
		generator = GenerateVectorsFromTweets()
		vector = generator.getVector_topics(tweets, self.lang)
		#se generan los vectores de todos los usuarios
		consultasNeo4j = ConsultasNeo4j()
		userID = consultas.getUserIDByScreenNameCassandra(self.usuario)
		seguidoresysiguiendo = consultasNeo4j.getSiguiendoOrSeguidosByUserID(userID)
		relaciones_coseno = []
		for user in seguidoresysiguiendo:
			tweets_ = consultas.getTweetsUsuarioCassandra_statusAndLang(user)
			vector_ = np.array([generator.getVector_topics(tweets, self.lang)]).T
			coseno = np.dot(vector, vector_)[0]
			relaciones_coseno.append((user, coseno))

		relaciones_coseno = sorted(relaciones_coseno, key=lambda x: x[1], reverse=True)

		with self.output().open('w') as out_file:
			for relacion in relaciones_coseno:
				out_file.write(str(relacion[0]))
				out_file.write("\n")
		