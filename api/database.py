import psycopg as db
import configparser
from api import dbtool.ini

def insert_into_table(valency, dance, energy, summary, ip_address, city, country):
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read(’dbtool.ini’)

    conn = db.connect(∗∗config[’connection’])
    curs = conn.cursor()

    curs.execute(”INSERT INTO mood VALUES (%s, %s, %s, %s, TIMESTAMP(NOW()), %s)”, (valency, dance, energy, summary, ip_address))
    curs.execute(”INSERT INTO location VALUES (%s, %s, %s)”, (ip_address, city, country))

    conn.close()