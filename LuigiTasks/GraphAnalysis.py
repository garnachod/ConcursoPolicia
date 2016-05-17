import luigi
import datetime
import networkx as nx

from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j

from Config.Conf import Conf

def remove_edges(g, in_degree=1):
		g2=g.copy()
		d_in=g2.in_degree(g2)
		d_out=g2.out_degree(g2)
		
		for n in g2.nodes():
			if d_in[n] <= in_degree: 
				g2.remove_node(n)
		
		return g2

class GenerateCommunityGraph(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		"""
		"""
		now = datetime.datetime.now()
	
		dia = now.day
		mes = now.month
		anyo = now.year
		try:
			usuario = self.usuario.replace("@", "")
			self.usuario = usuario
		except:
			pass
		#return luigi.LocalTarget('%s/LuigiTasks/graphs/gephi/%s/%s/%s_%s_%s'%(path, anyo, mes, self.usuario))
		return luigi.LocalTarget('%s/graphs/gephi/%s/%s/%s.gexf'%(path, anyo, mes, self.usuario))

	def run(self):
		consultas = ConsultasCassandra()
		consultasNeo = ConsultasNeo4j()

		user_id = consultas.getUserIDByScreenNameCassandra(self.usuario)
		seguidores_ini = consultasNeo.getListaIDsSeguidoresByUserID(user_id)
		DG=nx.DiGraph()

		#DG.add_edges_from([(seguidor_ini, user_id) for seguidor_ini in seguidores_ini])
		for seguidor_ini in seguidores_ini:
			siguiendo_seguidor = consultasNeo.getListaIDsSiguiendoByUserID(seguidor_ini)
			DG.add_edges_from([(seguidor_ini, siguiendo) for siguiendo in siguiendo_seguidor])

		with self.output().open("w") as fout:
			nx.write_gexf(DG, fout)

class AnalyticsCommunity(luigi.Task):
	"""
		Clase abstracta que solo necesita de un metodo de analisis y donde almacenarlo
	"""
	usuario = luigi.Parameter()

	def requires(self):
		return GenerateCommunityGraph(self.usuario)

	def getFolderAnalysis(self):
		raise NotImplementedError( "Should have implemented this" )

	def output(self):
		conf = Conf()
		path = conf.getAbsPath()
		"""
		"""
		now = datetime.datetime.now()
	
		dia = now.day
		mes = now.month
		anyo = now.year
		try:
			usuario = self.usuario.replace("@", "")
			self.usuario = usuario
		except:
			pass
		#return luigi.LocalTarget('%s/LuigiTasks/graphs/gephi/%s/%s/%s_%s_%s'%(path, anyo, mes, self.usuario))
		return luigi.LocalTarget('%s/graphs/%s/%s/%s/%s.gexf'%(path, self.getFolderAnalysis(), anyo, mes, self.usuario))

	def getComputedDictionary(self, graph):
		raise NotImplementedError( "Should have implemented this" )

	def run(self):
		consultas = ConsultasCassandra()
		DG = None
		with self.input().open("r") as fin:
			DG = nx.read_gexf(fin)

		DG = remove_edges(DG)
		page_rank = self.getComputedDictionary(DG)
		page_rank = [(key, page_rank[key]) for key in page_rank]
		page_rank = sorted(page_rank, key=lambda x: x[1], reverse = True)[:20]

		
		for user_id, value in page_rank:
			print consultas.getScreenNameByUserIDCassandra(long(user_id))


class PagerankCommunity(AnalyticsCommunity):
	"""
		extiende de AnalyticsCommunity, computa el pagerank:
			implementado getFolderAnalysis()
			implementado getComputedDictionary()
	"""
	def getFolderAnalysis(self):
		return "pagerank"

	def getComputedDictionary(self, graph):
		return nx.pagerank(graph)
	

class ClosenessCommunity(AnalyticsCommunity):
	"""
		extiende de AnalyticsCommunity, computa el pagerank:
			implementado getFolderAnalysis()
			implementado getComputedDictionary()
	"""
	def getFolderAnalysis(self):
		return "closeness"

	def getComputedDictionary(self, graph):
		return nx.closeness_centrality(graph)