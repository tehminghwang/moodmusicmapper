import psycopg as db
import configparser

def insert_into_database(cookies, valency, dance, energy, summary, time, ipaddress, city, country):
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read(’dbtool.ini’)

    conn = db.connect(∗∗config[’connection’])
    curs = conn.cursor()

    # Inserting into one table first for trial
    curs.execute(”INSERT INTO mood VALUES (%s, %s, %s, %s, %s, %s, %s)”, (cookies, valency, dance, energy, summary, time, ipaddress))
    curs.execute(”INSERT INTO location VALUES (%s, %s, %s)”, (ipaddress, city, country))

    conn.close()