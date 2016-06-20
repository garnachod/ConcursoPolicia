from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from ProcesadoresTexto.GenerateVectorsFromTweets import GenerateVectorsFromTweets

import numpy as np

if __name__ == '__main__':
	usuario = 'fondosur_1980'
	lang = 'es'


	consultas = ConsultasCassandra()
	tweets = consultas.getTweetsUsuarioCassandra_statusAndLang_noRT(usuario)
	print tweets
	generator = GenerateVectorsFromTweets()
	vector = generator.getVector_semantic(tweets, lang)
	#se generan los vectores de todos los usuarios
	consultasNeo4j = ConsultasNeo4j()
	userID = consultas.getUserIDByScreenNameCassandra(usuario)
	print userID
	seguidoresysiguiendo = consultasNeo4j.getListaIDsSeguidoresByUserID(userID)
	print seguidoresysiguiendo
	relaciones_coseno = []
	for user in seguidoresysiguiendo:
		tweets_ = consultas.getTweetsUsuarioCassandra_statusAndLang_noRT(user)
		vector_ = np.array([generator.getVector_semantic(tweets_, lang)]).T
		coseno = np.dot(vector, vector_)[0]
		relaciones_coseno.append((user, coseno))

	relaciones_coseno = sorted(relaciones_coseno, key=lambda x: x[1], reverse=True)

	with open('similitudes.txt','w') as out_file:
		for relacion in relaciones_coseno:
			out_file.write(str(relacion[0]))
			out_file.write("\n")