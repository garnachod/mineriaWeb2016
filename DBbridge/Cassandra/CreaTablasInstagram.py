from cassandra.cluster import Cluster

def creaUsers(session):
    query = (
             'CREATE TABLE users ('
             'id bigint PRIMARY KEY'
             ', username varchar'
             ', full_name varchar'
             ', followers int'
             ', following int'
             ', bio varchar'
             ', profile_picture varchar'
             ', last_media_collected bigint);'
            )
    session.execute(query)

def creaIndexUsers(session):
    query = "CREATE INDEX indx_username ON users (username);"
    session.execute(query)


if __name__ == '__main__':
    cluster = Cluster()
    session = cluster.connect('instagram')
    creaUsers(session)
    creaIndexUsers(session)