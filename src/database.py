import psycopg2 as psql
import config
from configparser import ConfigParser


# connect to the database
def connect(q):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psql.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(q)
        # get the result
        res = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psql.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            return res

# read the configuration of the database
def config(filename='../database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

