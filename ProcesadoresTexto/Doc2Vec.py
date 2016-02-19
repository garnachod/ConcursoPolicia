# gensim modules
from gensim import utils, matutils
from gensim.models.doc2vec import TaggedDocument
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from blist import blist
import gensim
import random
import time
import codecs
import numpy as np


class LabeledLineSentence(object):
	"""
		ides:
			Number	
			String
	"""
	def __init__(self, source, ides="Number"):
		self.source = source
		self.sentences = None
		self.ides = ides
		self.doc2vec = None
		
	def to_array(self):
		if self.sentences is None:
			self.sentences = blist()
			with utils.smart_open(self.source) as fIn:
				last_identif = 0
				for item_no, line in enumerate(fIn):
					line = line.replace("\n", "")
					if item_no % 2 == 0:
						if self.ides == "Number":
							last_identif = long(line)
						else:
							last_identif = line
					else:
						palabras = utils.to_unicode(line).split()
						palabras_clean = []
						for palabra in palabras:
							if len(palabra) > 1:
								palabras_clean.append(palabra)
						if len(palabras_clean) > 0:
							self.sentences.append(TaggedDocument(palabras_clean, [str(last_identif)]))
					
		return self.sentences
		

	def sentences_perm(self):
		random.shuffle(self.sentences)
		return self.sentences

class Doc2Vec(object):
	"""docstring for Doc2Vec"""
	def __init__(self):
		super(Doc2Vec, self).__init__()
		self.doc2vec = None
		
	def train(self,input_path, save_location, dimension = 50, epochs = 20, method="DBOW"):
		sentences = LabeledLineSentence(input_path)

		total_start = time.time()
		dm_ = 1 
		if method != "DBOW":
			dm_ = 0
		model = gensim.models.Doc2Vec(min_count=1, window=7, size=dimension, dm = dm_, sample=1e-3, negative=5,workers=6, alpha=0.04)
		
		print "inicio vocab"
		model.build_vocab(sentences.to_array())
		print "fin vocab"
		first_alpha = model.alpha
		last_alpha = 0.01
		next_alpha = first_alpha
		for epoch in range(epochs):
			start = time.time()
			print "iniciando epoca DBOW:"
			print model.alpha
			model.train(sentences.sentences_perm())
			end = time.time()
			next_alpha = (((first_alpha - last_alpha) / float(epochs)) * float(epochs - (epoch+1)) + last_alpha)
			model.alpha = next_alpha
			print "tiempo de la epoca " + str(epoch) +": " + str(end - start)

		model.save(save_location)

		total_end = time.time()

		print "tiempo total:" + str((total_end - total_start)/60.0)

	def simulateVectorsFromUsersFile(self, input_path, modelLocation):
		d2v =  gensim.models.Doc2Vec.load(modelLocation)
		sentences = LabeledLineSentence(input_path).to_array()
		dicUser_Vector = {}
		for sentence in sentences:
			palabras = sentence[0]
			user = sentence[1][0]
			vector = np.array(d2v.infer_vector(palabras, steps=3, alpha=0.1))
			dicUser_Vector[str(user)] = vector / np.linalg.norm(vector)

		return dicUser_Vector

	def simulateVectorsFromVectorText(self, vectorText, modelLocation):
		if self.doc2vec is None:
			self.doc2vec =  gensim.models.Doc2Vec.load(modelLocation)
		
		vector = np.array(self.doc2vec.infer_vector(vectorText, steps=3, alpha=0.1))
		return vector / np.linalg.norm(vector)