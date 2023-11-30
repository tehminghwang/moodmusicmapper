import psycopg as db
import configparser

def insert_into_table(valency, dance, energy, summary, ip_address, city, country):
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read('dbtool.ini')

    conn = db.connect(**config['connection'])
    curs = conn.cursor()

    curs.execute("""INSERT INTO location VALUES ('123.567.1252', 'London', 'United Kingdom')""")

    #curs.execute("""INSERT INTO mood VALUES (%s, %s, %s, %s, TIMESTAMP(NOW()), %s)""", (valency, dance, energy, summary, ip_address))
    #curs.execute("""INSERT INTO location VALUES (%s, %s, %s)""", (ip_address, city, country))

    conn.close()

def test_table():
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read('dbtool.ini')

    conn = db.connect(**config['connection'])
    curs = conn.cursor()

    curs.execute("""INSERT INTO test VALUES (%s, %s, %s);""", ("Bob Andy", 24, 1999))

    conn.close()