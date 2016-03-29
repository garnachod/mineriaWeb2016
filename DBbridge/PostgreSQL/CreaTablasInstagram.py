# -*- coding: utf-8 -*-
#import os
#import sys
#lib_path = os.path.abspath('../../')
#sys.path.append(lib_path)
from ConexionSQL import ConexionSQL



def crea_tablas():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS instagram_tokens CASCADE;'
             'CREATE TABLE instagram_tokens('
             'id serial PRIMARY KEY, '
             'api_key varchar(50), '
             'api_key_secret varchar(100)'
            ');'
        )
    cur.execute(query)

    query = ('DROP TABLE IF EXISTS instagram_tokens_count CASCADE;'
             'CREATE TABLE instagram_tokens_count('
             'id serial PRIMARY KEY, '
             'tiempo timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, '
             'id_token int REFERENCES instagram_tokens (id), '
             'simulado boolean DEFAULT false'
             ');'
             )
    cur.execute(query)

    query = 'INSERT into instagram_tokens (api_key, api_key_secret) VALUES (%s, %s);'

    cur.execute(query, ['24cd6d6d47a643e0b455da9ef27213b5', '6febde6916b1481dacdb213e155f766d'])

    conn.commit()

if __name__ == '__main__':
    crea_tablas()