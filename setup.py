#!/usr/bin/env python

from distutils.core import setup

setup(name='Proyecto Mineria',
      version='1.0',
      description='Sentimientos de menciones',
      author='Daniel Garnacho, Carlos Rosado',
      author_email='garnachod@gmail.com',
      packages=['API', 'Config', 'DBbridge', 'DBbridge.PostgreSQL', 'Cassandra', 'Neo4j', 'PostgreSQL', 'LuigiTasks', 'ProcesadoresTexto', 'SocialAPI','SocialAPI.TwitterAPI', 'spark'],
      package_dir={'Cassandra': 'DBbridge/Cassandra', 'Neo4j': 'DBbridge/Neo4j', 'PostgreSQL': 'DBbridge/PostgreSQL'},
    )
