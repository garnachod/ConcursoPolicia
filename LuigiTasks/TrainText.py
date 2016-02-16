# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import luigi

import datetime

from ClasificaUsuariosPorIdioma import *
from ProcesadoresTexto.Doc2Vec import Doc2Vec

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
		self.path = 'TrainText/Doc2VecLang_topics/%s/%s/%s.check'%(anyo, mes, dia)
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
		self.path = 'TrainText/Doc2VecLang_semantic/%s/%s/%s.check'%(anyo, mes, dia)
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


		
