<<<<<<< HEAD
#!/usr/bin/env python

from distutils.core import setup

setup(name='ConcursoPolicia',
      version='1.0',
      description='Buscador de usuarios en twitter',
      author='Daniel Garnacho',
      author_email='garnachod@gmail.com',
      packages=['AnnoyComparators', 'API', 'Config', 'DBbridge', 'DBbridge.PostgreSQL', 'Cassandra', 'Neo4j', 'PostgreSQL', 'LuigiTasks', 'ProcesadoresTexto', 'SocialAPI','SocialAPI.TwitterAPI', 'spark', 'website'],
      package_dir={'Cassandra': 'DBbridge/Cassandra', 'Neo4j': 'DBbridge/Neo4j', 'PostgreSQL': 'DBbridge/PostgreSQL'},
    )
=======
#!/usr/bin/env python

from distutils.core import setup

setup(name='ConcursoPolicia',
      version='1.0',
      description='Buscador de usuarios en twitter',
      author='Daniel Garnacho',
      author_email='garnachod@gmail.com',
      packages=['AnnoyComparators', 'API', 'Config', 'DBbridge', 'DBbridge.PostgreSQL', 'Cassandra', 'Neo4j', 'PostgreSQL', 'LuigiTasks', 'ProcesadoresTexto', 'SocialAPI','SocialAPI.TwitterAPI', 'spark', 'website'],
      package_dir={'Cassandra': 'DBbridge/Cassandra', 'Neo4j': 'DBbridge/Neo4j', 'PostgreSQL': 'DBbridge/PostgreSQL'},
    )
>>>>>>> 17cbacc00e3d3c0473322418579f3f2a74d3a6fc
