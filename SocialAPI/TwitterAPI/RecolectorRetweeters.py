# -*- coding: utf-8 -*-
from SocialAPI.Recolector import Recolector
from ApoyoTwitter import ApoyoTwitter
from getAuthorizations import GetAuthorizations
from twython import Twython
from time import time

class RecolectorRetweeters(Recolector):
	def __init__(self, escritor):
		super(RecolectorRetweeters, self).__init__(escritor)
		self.authorizator = GetAuthorizations(60)
		self.twitter = None
		self.apoyo = ApoyoTwitter()
		self.tipo_id = 7
		self.inicializa()

	def inicializa(self):
		self.authorizator.load_twitter_token(self.tipo_id)
		api_key, access_token = self.authorizator.get_twython_token()
		self.twitter = Twython(api_key, access_token=access_token)

	def recolecta(self, id_tweet):
		if id_tweet is None:
			raise Exception('The id of the tweet is None')


		tweets = self.privateRealizaConsulta(id_tweet)
		if tweets == []:
			return

		self.guarda(tweets)
	

	def guarda(self, datos):
		#print datos[0]
		for escritor in self.escritores:
			escritor.escribe(datos)
			if escritor is None:
				print datos[0]

	def privateRealizaConsulta(self, identificador):
		count = 100
		if self.authorizator.is_limit_api(self.tipo_id):
			raise Exception('LIMITE')

		try:
			retorno = self.twitter.get_retweets(id=identificador, count=count)
			self.authorizator.add_query_to_key(self.tipo_id)

			return retorno
		except Exception, e:
			print e
			self.authorizator.add_query_to_key(self.tipo_id)
			if "429" in str(e):
				raise Exception('LIMITE')

			return []

if __name__ == '__main__':
	r = RecolectorRetweeters([None])
	r.recolecta(631260309026553856)