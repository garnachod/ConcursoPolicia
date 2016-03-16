# ConcursoPolicia
Proyecto para el concurso de la policia, este código es el que se va entregar

## Planificación
![Alt text](./ImagesMD/primerSprint.png?raw=true "Primer Sprint")

Primera semana:
* Diego:
	* Elegir entre servidor Django o Flask o similar
	* Comenzar a materializar la Maqueta
* Dani:
	* Definir las APIs Python que usará la interfaz
	* Crear los módelos de textos por idioma

## Última versión de la maqueta
![Alt text](./ImagesMD/maqueta.png?raw=true "Primer Sprint")

## Instrucciones de instalación
* Instalar Cassandra: probado con Cassandra 2.1.11
	* Podía funcionar 2.1.13 sin cambiar nada
	* Podría funciona con otras versiones de Cassandra pero seguramente cambie alguna consulta
	* Crear keyspace twitter
* Instalar Neo4J: no hay problemas con la versión por ahora
	* Configurar la contraseña, si no cambiamos la de por defecto falla
* Instalar PostgreSQL
	* Crear dos Bases de datos (policia, twitter)
* Instalar https://github.com/Stratio/cassandra-lucene-index instalar la misma version que Cassandra
* Copiar Config/Conf_default.py con el nombre de Conf.py
	* Configurar los parametros correctos.
* Instalar las librerias de las que se compone el proyecto:
	* sudo python setup.py install
	* remove:
	* python setup.py install --record files.txt
	* cat files.txt | xargs rm -rf
* Lanzar creación de tablas:
	* DBbridge/Cassandra/Creatablas.py
	* DBbridge/Neo4j/CreaRelaciones.py
	* DBbridge/PostgreSQL/CreaTablas.py
* Instalar las librerías python:
	* Instalar dependencias con pip install -r requirements.txt
	* Creat tablas de Django con python manage.py migrate
* Configurar cronjobs
* Si Luigi se va a lanzar desde apache:
	* chown -R www-data:www-data LuigiTasks/