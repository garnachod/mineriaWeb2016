# -*- coding: iso-8859-15 -*-
import psycopg2
from DBbridge.PostgreSQL.ConexionSQL import ConexionSQL



class GetAuthorizations():
    def __init__(self, limit):
    	conSql = ConexionSQL()
        self.conn = conSql.getConexion()
        self.cur = conSql.getCursor()
        self.limit = limit

    def load_token(self):
     	query = "SELECT id FROM instagram_tokens;"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            query = "INSERT INTO instagram_tokens_count (id_token, simulado) VALUES (%s, true);"
            self.cur.execute(query, [row[0],])

        query = "SELECT id_token, count(id_token) as cuenta from (select id_token from instagram_tokens_count  where tiempo > current_timestamp - interval '15 minutes') as A  GROUP BY id_token order by cuenta Limit 1;"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            self.id = row[0]
            self.cuenta = row[1]


        query = "SELECT * FROM instagram_tokens WHERE id = %s;"
        self.cur.execute(query, (self.id,))
        rows = self.cur.fetchall()
        for row in rows:
            #self.id = row[0]
            self.api_key = row[1]
            self.api_key_secret = row[2]

    def add_query_to_key(self):
        query = "INSERT INTO instagram_tokens_count (id_token) VALUES (%s);"
        #comienzo de la transaccion
        self.cur.execute("BEGIN")    
        self.cur.execute(query, [self.id,])
        self.cur.execute("COMMIT")

    def set_limit_api(self, limit):
        self.limit = limit


     #mira a ver cuantas consultas se han realizado con ese apik
    def is_limit_api(self):
        query = "SELECT count(id_token) as cuenta from (select id_token from instagram_tokens_count where id_token = %s AND simulado = false AND tiempo > current_timestamp - interval '15 minutes') as A  GROUP BY id_token;"

        self.cur.execute(query, [self.id, ])
        row = self.cur.fetchone()
        try:
            if int(row[0]) >= self.limit:
                return True
            else:
                return False
        except Exception, e:
            return False

    def get_secret(self):
    	API_key = self.api_key
        API_secret = self.api_key_secret
        return [API_key, API_secret]