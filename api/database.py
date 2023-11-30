import psycopg2 as db
import configparser

def insert_into_table(ipaddress, input_mood, mood, valency, danceability, energy, city, country):
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read('dbtool.ini')

    conn = db.connect(**config['connection'])
    curs = conn.cursor()

    try:
        print("Executing SQL query...")
        curs.execute("""INSERT INTO mood VALUES (NOW(), %s, %s, %s, %s, %s, %s);""", (ipaddress, input_mood, mood, valency, danceability, energy))
        curs.execute("""INSERT INTO location VALUES (%s, %s, %s);""", (ipaddress, city, country))

        print("Committing transaction...")
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Closing connection...")
        conn.close()

def test_table():
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read('dbtool.ini')

    conn = db.connect(**config['connection'])
    curs = conn.cursor()

    try:
        print("Executing SQL query...")
        curs.execute("""INSERT INTO test VALUES (%s, %s, %s);""", ("Bob Andy", 24, 1999))

        print("Committing transaction...")
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Closing connection...")
        conn.close()