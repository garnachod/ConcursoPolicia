from annoy import AnnoyIndex
import json

class AnnoyModelTime(object):
	"""docstring for AnnoyModelTime"""
	def __init__(self, lang, folder):
		super(AnnoyModelTime, self).__init__()
		self.lang = lang
		self.folder = folder
		self.f = 24 * 7  # Length of item vector that will be indexed
	
	def train(self, tuples):
		"""
			array de tuplas (usuario, vector)
		"""
		
		t = AnnoyIndex(self.f)

		dic_index = {}
		for i, (user, vector) in enumerate(tuples):
		    t.add_item(i, vector)
		    dic_index[str(i)] = user

		t.build(20) # 20 trees
		t.save(self.folder +"/"+ self.lang + '.ann')
		with open(self.folder +"/"+ self.lang + '.json', "w") as fout:
			fout.write(json.dumps(dic_index))

	def getSimilar(self, vector, numberSim):
		with open(self.folder +"/"+ self.lang + '.json', "r") as fin:
			dicInverse = json.loads(fin.read())

		u = AnnoyIndex(self.f)
		u.load(self.folder +"/"+ self.lang + '.ann')

		similarElem, values = u.get_nns_by_vector(vector, 50000, include_distances=True)

		best = []
		for i in xrange(numberSim):
			best.append(dicInverse[str(similarElem[i])])

		return best
		