# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import luigi
from GeneradorDocumentosTwitter import *
import gensim
from blist import blist
import codecs
import numpy



class LDATwitterUser(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextos LDATwitterUser --usuario ...
	"""
	usuario = luigi.Parameter()
	idioma = luigi.Parameter(default="es")

	def output(self):
		return luigi.LocalTarget(path='textos/LDATwitterUser(%s)'%self.usuario)

	def requires(self):
		return GeneradorTextoUsuario(self.usuario)

	def run(self):
		tweets = blist([])

		with self.input().open('r') as in_file:
			for line in in_file:
				palabras = line.replace("\n", "").split()
				if len(palabras) > 2:
					tweets.append(palabras)


		print len(tweets)

		dictionary = gensim.corpora.Dictionary([doc for doc in tweets])
		dictionary.compactify()
		dictionary.save("textos/dictionary_%s.dict"%self.usuario)

		corpus = [dictionary.doc2bow(doc) for doc in tweets]
		gensim.corpora.MmCorpus.serialize('textos/corpus_%s.mm'%self.usuario, corpus)

		#corpus = gensim.corpora.MmCorpus('test.mm')
		#dictionary = gensim.corpora.Dictionary.load("dictionary.dict")

		print "entrenando"
		#lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=50, distributed=True)
		lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=7, chunksize=200000, passes=500, alpha='auto')

		lda.save('textos/model_%s.lda'%self.usuario)


		with self.output().open('w') as out_file:
			out_file.write("OK")

class LDATwitterUserSinLem(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextos LDATwitterUserSinLem --usuario ...
	"""
	usuario = luigi.Parameter()
	idioma = luigi.Parameter(default="es")

	def output(self):
		return luigi.LocalTarget(path='textos/LDATwitterUserSinLem(%s)'%self.usuario)

	def requires(self):
		return GeneradorTextoUsuarioSinLem(self.usuario)

	def run(self):
		tweets = blist([])

		with self.input().open('r') as in_file:
			for line in in_file:
				palabras = line.replace("\n", "").split()
				if len(palabras) > 2:
					tweets.append(palabras)


		print len(tweets)

		dictionary = gensim.corpora.Dictionary([doc for doc in tweets])
		dictionary.compactify()
		dictionary.save("textos/dictionary_nolem_%s.dict"%self.usuario)

		corpus = [dictionary.doc2bow(doc) for doc in tweets]
		gensim.corpora.MmCorpus.serialize('textos/corpus_nolem_%s.mm'%self.usuario, corpus)

		#corpus = gensim.corpora.MmCorpus('test.mm')
		#dictionary = gensim.corpora.Dictionary.load("dictionary.dict")

		print "entrenando"
		#lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=50, distributed=True)
		lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=7, chunksize=200000, passes=500, alpha='auto')

		lda.save('textos/model_nolem_%s.lda'%self.usuario)


		with self.output().open('w') as out_file:
			out_file.write("OK")
