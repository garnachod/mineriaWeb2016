from cassandra.cluster import Cluster

def creaUsersTwitter(session):
    query = (
             'CREATE TABLE users ('
             'id_twitter bigint PRIMARY KEY'
             ', name varchar'
             ', screen_name varchar'
             ', followers int'
             ', following int'
             ', location varchar'
             ', created_at timestamp '
             ', profile_img varchar'
             ', last_tweet_collected bigint);'
            )
    session.execute(query)

def creaIndexUsersTwitter(session):
    query = "CREATE INDEX indx_screen_name ON users (screen_name);"
    session.execute(query)

def getSchemas(session):
    query = "SELECT * FROM system.schema_keyspaces;"
    print session.execute(query)
def getTables(session):
    query = "select columnfamily_name from system.schema_columnfamilies where keyspace_name = 'twitter';"
    print session.execute(query)

def creaTweets(session):
    query = ('CREATE TABLE Tweets ('
             'id_twitter bigint'
             ', status text'
             ', tuser bigint'
             ', created_at timestamp'
             ', lang text'
             ', orig_tweet bigint'
             ', favorite_count int'
             ', retweet_count int'
             ', media_urls map<text, text>'
             ', latitude FLOAT'
    		 ', longitude FLOAT'
             ', lucene TEXT'
             ', PRIMARY KEY (tuser, id_twitter)'
             ')WITH CLUSTERING ORDER BY (id_twitter DESC);'
             
    )
    session.execute(query)

def creaIndexTweet(session):
    ###usa el plugin "https://github.com/Stratio/cassandra-lucene-index" que usa LUCENE
    query = "DROP INDEX tweets_index;"
    session.execute(query)
    query = (
        "CREATE CUSTOM INDEX tweets_index ON tweets (lucene)"
        "USING 'com.stratio.cassandra.lucene.Index'"
        "WITH OPTIONS = {"
        "'refresh_seconds' : '60',"
        "'schema' : '{"
        "fields : {"
        "   id_twitter : {type : \"bigint\"},"
        "   tuser  : {type : \"bigint\"},"
        "   orig_tweet: {type : \"bigint\"},"
        "   status  : {type : \"text\", analyzer : \"english\"},"
        "   created_at  : {type : \"date\", pattern : \"yyyy-MM-dd HH:mm:ss\",sorted:true},"
        " place : {type : \"geo_point\", latitude:\"latitude\", longitude:\"longitude\"}"
        "}"
    "}'"
    "};"
    )
    session.execute(query)
    """
    query = "CREATE INDEX indx_id_twitter ON tweets (id_twitter);"
    session.execute(query)
    query = "CREATE INDEX indx_orig_tweet ON tweets (orig_tweet);"
    session.execute(query)
    query = "CREATE INDEX indx_lang ON tweets (lang);"
    session.execute(query)"""


def debug_func(session):
    query = "select * from system.schema_columnfamilies where keyspace_name = 'twitter';"
    print session.execute(query)


def clean(session):
    session.execute("DROP TABLE Tweets;")
    session.execute("DROP TABLE users;")
def clean_tweets(session):
    session.execute("DROP TABLE Tweets;")


def alterTableUser(session):
	#friends_count
	query = "ALTER TABLE users ADD following int;"
	session.execute(query)
	

    
if __name__ == '__main__':
    cluster = Cluster()
    session = cluster.connect('twitter')
    debug = True
    if debug:
    	#alterTableUser(session)
        #clean_tweets(session)
        #creaTweets(session)
        creaIndexTweet(session)
    else:
        clean(session)
        creaUsersTwitter(session)
        creaIndexUsersTwitter(session)
        #print "************usuario creado **************"
        creaTweets(session)
        creaIndexTweet(session)
        
        #print "************tweet creado **************"
        getSchemas(session)
        getTables(session)
    