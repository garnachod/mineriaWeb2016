#!/usr/bin/env python

from distutils.core import setup

setup(name='ConcursoPolicia',
      version='1.0',
      description='Buscador de usuarios en twitter',
      author='Daniel Garnacho',
      author_email='garnachod@gmail.com',
      packages=['AnnoyComparators', 'API', 'Config', 'DBbridge', 'DBbridge.PostgreSQL', 'Cassandra', 'Neo4j', 'PostgreSQL', 'LuigiTasks', 'ProcesadoresTexto', 'SocialAPI','SocialAPI.TwitterAPI', 'spark'],
      package_dir={'Cassandra': 'DBbridge/Cassandra', 'Neo4j': 'DBbridge/Neo4j', 'PostgreSQL': 'DBbridge/PostgreSQL'},
    )
