# -*- coding: utf-8 -*-
from ConexionSQL import ConexionSQL


def crea_tablas():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS Users CASCADE;'
             'CREATE TABLE Users ('
             ' id_twitter bigint PRIMARY KEY'
             ', name varchar(20)'
             ', screen_name varchar(15)'
             ', followers int'
             ', location varchar(50)'
             ', created_at date'
             ', last_tweet_collected bigint'  # puede no ser el ultimo, sino el ultimo recogido sistemáticamente del usuario
             ');'
             #'CREATE UNIQUE INDEX CONCURRENTLY users_idx ON Users(id_twitter);'
             'CREATE UNIQUE INDEX users_sn_idx ON Users(screen_name);'
    )
    cur.execute(query)
    query = ('DROP TABLE IF EXISTS Tweets CASCADE;'
             'CREATE TABLE Tweets ('
             ' id_twitter bigint PRIMARY KEY'
             ', status varchar(160)'
             ', tuser bigint'
             ', created_at timestamp'
             ', lang char(3)'
             ', is_retweet boolean'
             ', orig_tweet bigint'
             ', favorite_count int'
             ', retweet_count int'
             ', media_url varchar(100)'
             ');'
             #'CREATE UNIQUE INDEX CONCURRENTLY ON  tweets (id_twitter);'
             'CREATE INDEX tweets_tu_idx ON Tweets (tuser);'
    )
    cur.execute(query)

    query = ('DROP TABLE IF EXISTS twitter_tokens CASCADE;'
             'CREATE TABLE twitter_tokens('
             'id serial PRIMARY KEY, '
             'api_key varchar(50), '
             'api_key_secret varchar(100), '
             'access_token varchar(100), '
             'access_token_secret varchar(100), '
             'oauth varchar(200)'
            ');'
             )
    cur.execute(query)
    conn.commit()

def crea_tokens_count():
    """Se ha visto que no se necesita indice (empeora el tiempo), al menos por ahora"""
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS tokens_count CASCADE;'
             'CREATE TABLE tokens_count('
             'id serial PRIMARY KEY, '
             'tiempo timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, '
             'id_token int REFERENCES twitter_tokens (id), '
             'id_tipo_query int, '
             'simulado boolean DEFAULT false'
             ');'
             )
    cur.execute(query)

    conn.commit()
    


def temp_crea_tablas():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS app_users CASCADE;'
             'CREATE TABLE app_users ('
             'id serial PRIMARY KEY'
             ', mail varchar(50)'
             ', name varchar(100)'
             ', institution varchar(30)'
             ', role varchar(20)'
             ', username varchar(20)'
             ', pasw varchar(100)'
             ');'
             'CREATE INDEX app_users_username ON app_users (username);'
             )
    cur.execute(query)
    
    query = ('DROP TABLE IF EXISTS app_searches CASCADE;'
             'CREATE TABLE app_searches ('
             'id serial PRIMARY KEY'
             ', search_string varchar(200)'
             ', id_user integer REFERENCES app_users(id)'
             ', number_new_tweets integer'
             ', number_recalled_tweets integer'
             ', search_time double precision'
             ');'
             )
    cur.execute(query)
   
    query = ('DROP TABLE IF EXISTS join_search_tweet CASCADE;'
             'CREATE TABLE join_search_tweet ( '
             'id_search int references app_searches(id), '
             'id_tweet bigint, '
             'primary key (id_search, id_tweet)'
             ');')
    cur.execute(query)
    
    conn.commit()


def crea_def_user():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()
    
    query = "INSERT INTO app_users (name,mail,institution,role,username,pasw) VALUES ('dani','garnachod@gmail.com','uam','admin','garnachod','58a543c86d0af40db318dec6c8b47e8a48dac9ea576ed5b944f07ec589e13fc5');"

    cur.execute(query)
    conn.commit()


def crea_tareas():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS tareas_programadas CASCADE;'
             'CREATE TABLE tareas_programadas ('
             'id serial PRIMARY KEY'
             ', tipo varchar(30)'
             ', id_search integer REFERENCES app_searches(id)'
             ', tiempo_inicio timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP '
             ', tiempo_fin timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP '
             ', ejecutar_cada_minutos int NOT NULL DEFAULT 5 '
             ', id_lista_entrenamiento int'
             ');'
             )
    cur.execute(query)
    
    conn.commit()


def crea_tabla_MLT():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS tweets_entrenamiento CASCADE;'
             'CREATE TABLE tweets_entrenamiento ('
             'id serial PRIMARY KEY'
             ', id_tweet bigint'
             ', id_lista integer REFERENCES listas_entrenamiento(id) ON DELETE CASCADE'
             ', fecha_creacion timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP '
             ', clase varchar(30)'
             ');'
             )
    cur.execute(query)
    
    conn.commit()


def crea_tabla_entrenamientos():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS entrenamientos CASCADE;'
             'CREATE TABLE entrenamientos ('
             'id serial PRIMARY KEY'
             ', fecha timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP '
             ', tipo varchar(30)'
             ', fichero_arff varchar(200)'
             ', fichero_json varchar(200)'
             ', porcentaje_fallo double precision'
             ', id_lista_entrenamiento int'
             ');'
             )
    cur.execute(query)
    
    conn.commit()


def crea_tabla_clasificacion():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS clasificacionTweets CASCADE;'
             'CREATE TABLE clasificacionTweets ('
             'id_tweet integer PRIMARY KEY'
             ', clase varchar(30)'
             ');'
             )
    cur.execute(query)
    
    conn.commit()


def crea_tabla_lista_entrenamiento():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS listas_entrenamiento CASCADE;'
             'CREATE TABLE listas_entrenamiento ('
             'id serial PRIMARY KEY'
             ', nombre varchar(140)'
             ', id_username integer REFERENCES app_users(id)'
             ');'
             )
    cur.execute(query)
    
    conn.commit()


def crea_tabla_seguidores():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS seguidores CASCADE;'
             'CREATE TABLE seguidores ('
             '  id_user int'
             ', id_seguidor int'
             ', fecha timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP '
             ', indice_captura int'
             ', primary key (id_user, id_seguidor)'
             ');'
             )
    cur.execute(query)
    
    conn.commit()


def crea_tablas_close():
	conSql = ConexionSQL()
	conn = conSql.getConexion()
	conn.close()

if __name__ == "__main__":
    debug = True
    if debug:
        #crea_tabla_MLT()
        crea_tareas()
        #crea_tokens_count()
    else:
        crea_tablas()
        temp_crea_tablas()
        crea_tokens_count()
        crea_def_user()
        crea_tareas()
        crea_tabla_lista_entrenamiento()
        crea_tabla_MLT()
        crea_tabla_entrenamientos()
        crea_tabla_clasificacion()
        crea_tabla_seguidores()
        crea_tablas_close()
    
    #crea_tabla_MLT()
    #crea_tabla_lista_entrenamiento()