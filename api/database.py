import psycopg as db
import configparser

# read in configuration file parameters from dbtool . ini
config = configparser.ConfigParser()
config.read(’dbtool.ini’)

conn = db.connect(∗∗config[’connection’])
curs = conn.cursor()

curs.execute(”””INSERT
”””,
[”GB”])
rec = curs.fetchone()
print(rec)

conn.close()