# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import luigi
from ClasificaUsuariosPorIdioma import *
from ProcesadoresTexto.Doc2Vec import Doc2Vec
from annoy import AnnoyIndex

import json
import datetime

class TrainDoc2VecLang_topics(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module TrainText TrainDoc2VecLang_topics --idioma ar
	"""
	idioma = luigi.Parameter()

	def output(self):
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		self.path = 'TrainText/Doc2VecLang_topics/%s/%s/%s_%s.check'%(anyo, mes, dia, self.idioma)
		return luigi.LocalTarget(path=self.path)

	def requires(self):
		return GeneraTextoPorIdioma_topics(self.idioma)

	def run(self):
		with self.output().open("w") as out:
			d2v = Doc2Vec()
			savePath = self.path.replace("check","model")
			print self.input().path
			d2v.train(self.input().path, savePath, dimension = 50, epochs = 20, method="DBOW")
			out.write("OK")

class TrainDoc2VecLang_semantic(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module TrainText TrainDoc2VecLang_semantic --idioma ar
	"""
	idioma = luigi.Parameter()

	def output(self):
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		self.path = 'TrainText/Doc2VecLang_semantic/%s/%s/%s_%s.check'%(anyo, mes, dia, self.idioma)
		return luigi.LocalTarget(path=self.path)

	def requires(self):
		return GeneraTextoPorIdioma_semantic(self.idioma)

	def run(self):
		with self.output().open("w") as out:
			d2v = Doc2Vec()
			savePath = self.path.replace("check","model")
			print self.input().path
			d2v.train(self.input().path, savePath, dimension = 50, epochs = 20, method="DM")
			out.write("OK")

class GenerateVecsAnnoyLang_topics(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module TrainText GenerateVecsAnnoyLang_topics --idioma ar
	"""
	idioma = luigi.Parameter()
	def output(self):
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget(path='AnnoyVecs/topics/%s/%s/%s_%s.json'%(anyo, mes, dia, self.idioma))

	def requires(self):
		return [GeneraTextoPorIdioma_topics(self.idioma), TrainDoc2VecLang_topics(self.idioma)]

	def run(self):
		text_loc = ""
		ModelLocation = ""
		for input in self.input():
			if "users_idiomas" in input.path:
				text_loc = input.path
			else:
				ModelLocation = input.path.replace("check","model")

		####
		# CUIDADO F esta fijado, debe ser igual que las dimensiones del modelo
		####
		f = 50
		t = AnnoyIndex(f)
		print "cargando modelo"
		d2v = Doc2Vec()
		dic_users_vectos = d2v.simulateVectorsFromUsersFile(text_loc, ModelLocation)
		# diccionario que traduce de id para annoy a id de usuario de twitter
		dic_users_id = {}
		count_users = 0
		for user in dic_users_vectos:
			t.add_item(count_users, dic_users_vectos[user])
			dic_users_id[user] = count_users
			count_users += 1
		print "entrenando annoy"
		t.build(20)
		with self.output().open("w") as f_out:
			f_out.write(json.dumps(dic_users_id))
			now = datetime.datetime.now()
			dia = now.day
			mes = now.month
			anyo = now.year
			path = 'AnnoyVecs/topics/%s/%s/%s_%s.json'%(anyo, mes, dia, self.idioma)
			t.save(path.replace("json","annoy"))

class GenerateVecsAnnoyLang_semantic(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module TrainText GenerateVecsAnnoyLang_topics --idioma ar
	"""
	idioma = luigi.Parameter()
	def output(self):
		now = datetime.datetime.now()
		dia = now.day
		mes = now.month
		anyo = now.year
		return luigi.LocalTarget(path='AnnoyVecs/semantic/%s/%s/%s_%s.json'%(anyo, mes, dia, self.idioma))

	def requires(self):
		return [GeneraTextoPorIdioma_semantic(self.idioma), TrainDoc2VecLang_semantic(self.idioma)]

	def run(self):
		text_loc = ""
		ModelLocation = ""
		for input in self.input():
			if "users_idiomas" in input.path:
				text_loc = input.path
			else:
				ModelLocation = input.path.replace("check","model")

		####
		# CUIDADO F esta fijado, debe ser igual que las dimensiones del modelo
		####
		f = 50
		t = AnnoyIndex(f)
		print "cargando modelo"
		d2v = Doc2Vec()
		dic_users_vectos = d2v.simulateVectorsFromUsersFile(text_loc, ModelLocation)
		# diccionario que traduce de id para annoy a id de usuario de twitter
		dic_users_id = {}
		count_users = 0
		for user in dic_users_vectos:
			t.add_item(count_users, dic_users_vectos[user])
			dic_users_id[user] = count_users
			count_users += 1
		print "entrenando annoy"
		t.build(20)
		with self.output().open("w") as f_out:
			f_out.write(json.dumps(dic_users_id))
			now = datetime.datetime.now()
			dia = now.day
			mes = now.month
			anyo = now.year
			path = 'AnnoyVecs/semantic/%s/%s/%s_%s.json'%(anyo, mes, dia, self.idioma)
			t.save(path.replace("json","annoy"))
		
		