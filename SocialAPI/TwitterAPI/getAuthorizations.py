# -*- coding: iso-8859-15 -*-
import psycopg2
from DBbridge.PostgreSQL.ConexionSQL import ConexionSQL


#queue = multiprocessing.Manager()
#queue.start()
class GetAuthorizations():
    def __init__(self, limit):
        conSql = ConexionSQL()
        self.conn = conSql.getConexion()
        self.cur = conSql.getCursor()
        self.limit = limit


    def load_twitter_token(self, tipo_id):
        query = "SELECT id FROM twitter_tokens;"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            query = "INSERT INTO tokens_count (id_token, id_tipo_query, simulado) VALUES (%s, %s,true);"
            self.cur.execute(query, [row[0],tipo_id])

        query = "SELECT id_token, count(id_token) as cuenta from (select id_token from tokens_count  where id_tipo_query = %s AND tiempo > current_timestamp - interval '15 minutes') as A  GROUP BY id_token order by cuenta Limit 1;"
        self.cur.execute(query, [tipo_id, ])
        rows = self.cur.fetchall()
        for row in rows:
            self.id = row[0]
            self.cuenta = row[1]


        query = "SELECT * FROM twitter_tokens WHERE id = %s;"
        self.cur.execute(query, (self.id,))
        rows = self.cur.fetchall()
        for row in rows:
            #self.id = row[0]
            self.api_key = row[1]
            self.api_key_secret = row[2]
            self.access_token = row[3]
            self.access_token_secret = row[4]
            self.oauth = row[5]

    def add_query_to_key(self, tipo):
        query = "INSERT INTO tokens_count (id_token, id_tipo_query) VALUES (%s,%s);"
        #comienzo de la transaccion
        self.cur.execute("BEGIN")    
        self.cur.execute(query, [self.id,tipo])
        self.cur.execute("COMMIT")

    def set_limit_api(self, limit):
        self.limit = limit

    #mira a ver cuantas consultas se han realizado con ese apik
    def is_limit_api(self, tipo):
        query = "SELECT count(id_token) as cuenta from (select id_token from tokens_count where id_token = %s AND id_tipo_query = %s AND simulado = false  AND tiempo > current_timestamp - interval '15 minutes') as A  GROUP BY id_token;"

        self.cur.execute(query, [self.id, tipo])
        row = self.cur.fetchone()
        try:
            if int(row[0]) >= self.limit:
                return True
            else:
                return False
        except Exception, e:
            return False

    def get_twitter_secret(self):
        API_key = self.api_key
        API_secret = self.api_key_secret
        access_token = self.access_token
        access_token_secret = self.access_token_secret
        return [API_key, API_secret, access_token, access_token_secret]
    """
    def get_tweepy_api_auth(self):
        API_key, API_secret, access_token, access_token_secret = get_twitter_secret()
        auth = tweepy.OAuthHandler(API_key, API_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    """
    def get_twython_token(self):
        API_key = self.api_key
        access_token = self.oauth
        return [API_key, access_token]

    def get_twython_token_auth(self):
        API_key = self.api_key
        API_secret = self.api_key_secret
        return [API_key, API_secret]    

    def get_yahoo_geo_api_auth():
        return '1Uo7bs_V34FrwQuJJywk5PKHc8VAcm.Hy_jN6.X.rr4CSOVELWsnBdb2BJV8lpFBPUksgHT.GkudoeLnEs6L_w--'
'''
def load_twitter_tokens():
    global twitter_tokens
    f = open("../secret/TwitterTokens.txt", "r")
    twitter_tokens = []
    for x in range(1, max_twitter_app):
        twitter_tokens.append([f.readline()[:-1], f.readline()[:-1], f.readline()[:-1], f.readline()[:-1], f.readline()[:-1]])
        
    f.close()

#todo: llevar cuenta de queries x window?
'''

'''
def get_tweepy_api_auth():
    API_key, API_secret, access_token, access_token_secret = get_twitter_secret()
    auth = tweepy.OAuthHandler(API_key, API_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

def get_twython_token():
    global next_twitter_app
    API_key = twitter_tokens[next_twitter_app][0]
    #API_secret = twitter_tokens[next_twitter_app][1]
    #access_token = twitter_tokens[next_twitter_app][2]
    access_token = twitter_tokens[next_twitter_app][4]
    next_twitter_app = (next_twitter_app + 1) % max_twitter_app
    print API_key
    print access_token
    return [API_key, access_token]

def get_twython_token_auth():
    API_key = twitter_tokens[next_twitter_app][0]
    API_secret = twitter_tokens[next_twitter_app][1]
    return [API_key, API_secret]

def get_yahoo_geo_api_auth():
    return '1Uo7bs_V34FrwQuJJywk5PKHc8VAcm.Hy_jN6.X.rr4CSOVELWsnBdb2BJV8lpFBPUksgHT.GkudoeLnEs6L_w--'
'''


