import psycopg2 as db
import configparser
from dotenv import load_dotenv
import os

def location_into_table(ipaddress, city, country):
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read('dbtool.ini')

    if os.getenv("VERCEL"):
    # Load environment variables from Vercel secrets
        password = os.environ.get('DATABASE_KEY')
    else:
    # Load environment variables from the .env file
        load_dotenv()
        password = os.environ.get("DATABASE")

    config['connection']['password'] = password

    conn = db.connect(**config['connection'])
    curs = conn.cursor()

    try:
        print("Executing SQL query...")
        curs.execute("""INSERT INTO location VALUES (%s, %s, %s);""", (ipaddress, city, country))

        print("Committing transaction...")
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Closing connection...")
        conn.close()

def mood_into_table(ipaddress, input_mood, mood, valency, danceability, energy, playlist):
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read('dbtool.ini')

    if os.getenv("VERCEL"):
    # Load environment variables from Vercel secrets
        password = os.environ.get('DATABASE_KEY')
    else:
    # Load environment variables from the .env file
        load_dotenv()
        password= os.environ.get("DATABASE")

    config['connection']['password'] = password

    conn = db.connect(**config['connection'])
    curs = conn.cursor()

    try:
        print("Executing SQL query...")
        curs.execute("""INSERT INTO mood VALUES (NOW(), %s, %s, %s, %s, %s, %s);""", (ipaddress, input_mood, mood, valency, danceability, energy))

        for item in playlist:
            curs.execute("""INSERT INTO spotify VALUES (NOW(), %s, %s, %s, %s);""", (ipaddress, item['name'], item['artist'], item['uri']))

        print("Committing transaction...")
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Closing connection...")
        conn.close()

def song_of_day():
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read('dbtool.ini')

    if os.getenv("VERCEL"):
    # Load environment variables from Vercel secrets
        password = os.environ.get('DATABASE_KEY')
    else:
    # Load environment variables from the .env file
        load_dotenv()
        password= os.environ.get("DATABASE")

    config['connection']['password'] = password

    conn = db.connect(**config['connection'])
    curs = conn.cursor()

    try:
        # Execute the SQL query
        print("Executing SQL query...")
        curs.execute("""SELECT DISTINCT uri, title, artist, COUNT(uri) OVER (PARTITION BY uri) AS frequency 
                    FROM spotify 
                    WHERE time >= now() - interval '24 hours' 
                    ORDER BY frequency DESC LIMIT 1;"""
                     )

        # Fetch the result
        result = curs.fetchone()

        if result:
            print(result)
        else:
            print("No result found")
    finally:
        # Close the cursor and connection
        curs.close()
        conn.close()

        return result[0];

def city_song_of_day():
    # read in configuration file parameters from dbtool.ini
    config = configparser.ConfigParser()
    config.read('dbtool.ini')

    conn = db.connect(**config['connection'])
    curs = conn.cursor()

    try:
        # Execute the SQL query
        print("Executing SQL query...")
        curs.execute("""SELECT DISTINCT uri, title, artist, COUNT(uri) OVER (PARTITION BY uri) AS frequency 
                    FROM spotify 
                    WHERE time >= now() - interval '24 hours' 
                    ORDER BY frequency DESC LIMIT 1;"""
                     )

        # Fetch the result
        result = curs.fetchone()

        if result:
            print(result)
        else:
            print("No result found")
    finally:
        # Close the cursor and connection
        curs.close()
        conn.close()

        return result[0];
