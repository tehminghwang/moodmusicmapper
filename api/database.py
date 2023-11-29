import psycopg as db
import configparser
import request

def insert_into_table(valency, dance, energy, summary, city, country):
    # read in configuration file parameters from dbtool.ini
    ipaddress = request.headers.get('x-real-ip') or request.headers.get('x-forwarded-for', request.remote_addr)

    config = configparser.ConfigParser()
    config.read(’dbtool.ini’)

    conn = db.connect(∗∗config[’connection’])
    curs = conn.cursor()

    # Inserting into one table first for trial
    curs.execute(”INSERT INTO mood VALUES (%s, %s, %s, %s, TIMESTAMP(NOW()), %s)”, (valency, dance, energy, summary, ipaddress))
    curs.execute(”INSERT INTO location VALUES (%s, %s, %s)”, (ipaddress, city, country))

    conn.close()