# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasCassandra import ConsultasCassandra
import codecs

if __name__ == '__main__':
	consultas = ConsultasCassandra()
	tweets = consultas.getTweetsUsuarioCassandra("@chicageo68", limit=100000)

	with codecs.open("chicageo68", "w", "utf-8") as fout:
		for tweet in tweets:
			fout.write(tweet.status.replace("\n", ". ").replace("\r", ". ").replace(u"\u0085", ". ").replace(u"\u2028", ". ").replace(u"\u2029", ". "))
			fout.write("\n")
