### Analisis de grafos
GraphAnalusis.py contiene la funcionalidad básica para estos analisis

#### GenerateCommunityGraph
Genera un grafo y lo guarda en formato Gephi

#### AnalyticsCommunity
Es una clase abstracta a la que hay que implementar 2 métodos, recorta los nodos que son seguidos por menos de una persona en la comunidad
* getFolderAnalysis, retorna una cadena del estilo "carpeta" donde se guardará el analisis
* getComputedDictionary, retorna un diccionario en formato networkx con el analisis

siguiendo este estilo podemos crear tantos análisis diferentes con apenas 10 lineas de código, por ejemplo ver método PagerankCommunity