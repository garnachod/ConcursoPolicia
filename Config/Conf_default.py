from collections import namedtuple

class Conf():
	"""docstring for SparkContexto"""
	class __impl:
		"""docstring for __impl"""
		def __init__(self):
			#dominio web (sin "http://" ni "/" final)
			self.domain = '0.0.0.0:8000'

			#cassandra
			self.cassandra_keyspace = 'twitter'
			self.cassandra_keyspace_instagram = 'instagram'
			self.cassandra_servers = ["127.0.0.1"]
			#SQL
			self.sql_database = 'twitter'
			self.sql_database_policia = 'policia'
			self.sql_user = 'tfg'
			self.sql_password = 'postgres_tfg'
			self.sql_host = 'localhost'
			self.sql_port = '5432'
			#app
			self.abspath = '/home/dani/github/ConcursoPolicia'
			#SPARK
			self.spark_home = '/home/dani/spark-1.4.0'
			#Neo4j
			self.neo4j_password = 'tfg_neo4j'
			self.neo4j_url = "localhost"
			#vectors
			self.dimVectors = 200

			#venv set "" if not venv
			self.venv_path = ""

		def getDomain(self):
			return self.domain

		def getCassandraKeyspace(self):
			return self.cassandra_keyspace

		def getCassandraKeyspaceInstagram(self):
			return self.cassandra_keyspace_instagram

		def getCassandraServers(self):
			return self.cassandra_servers

		def getSparkHome(self):
			return self.spark_home

		def getAbsPath(self):
			return self.abspath

		def getSQLInfo(self):
			infoSQL = namedtuple('InfoSQL', 'database, user, password, host')
			return infoSQL(self.sql_database, self.sql_user, self.sql_password, self.sql_host)

		def getSQLPoliceInfo(self):
			infoSQL = namedtuple('InfoSQL', 'database, user, password, host, port')
			return infoSQL(self.sql_database_policia, self.sql_user, self.sql_password, self.sql_host, self.sql_port)

		def getNeo4jPassword(self):
			return self.neo4j_password

		def getNeo4jUrl(self):
			return self.neo4j_url

		def getDimVectors(self):
			return self.dimVectors

		def getAnnoyTimePath(self):
			return self.annoyTimePath

		def getVenvPath(self):
			return self.venv_path




	# storage for the instance reference
	__instance = None

	def __init__(self):
		if Conf.__instance is None:
			Conf.__instance = Conf.__impl()

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)
