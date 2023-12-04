import psycopg2 as db
import configparser
from dotenv import load_dotenv
import os

# Inserts location data from this session into database.
def location_into_table(ipaddress, city, country, country_code):
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
        curs.execute("""INSERT INTO location VALUES (%s, %s, %s, %s);""", (ipaddress, city, country, country_code))
        print("Committing transaction...")
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Closing connection...")
        conn.close()

# Inserts user input and OpenAI output into database.
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
        password = os.environ.get("DATABASE")

    config['connection']['password'] = password

    conn = db.connect(**config['connection'])
    curs = conn.cursor()

    try:
        print("Executing SQL query...")
        curs.execute("""INSERT INTO mood VALUES (NOW(), %s, %s, %s, %s, %s, %s);""",
                     (ipaddress, input_mood, mood, valency, danceability, energy))

        for item in playlist:
            curs.execute("""INSERT INTO spotify VALUES (NOW(), %s, %s, %s, %s, %s);""",
                         (ipaddress, item['name'], item['artist'], item['uri'], item['artist_uri']))

        print("Committing transaction...")
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Closing connection...")
        conn.close()

# Returns URI of top recommended song of past 24 hours.
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
        password = os.environ.get("DATABASE")

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

# Returns all cities (and corresponding country) that have used the app in the past 24 hours.
def city_clients():
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
        # Execute the SQL query
        print("Executing SQL query...")
        curs.execute("""SELECT DISTINCT city, country
                    FROM location JOIN spotify
                    ON location.ipaddress = spotify.ipaddress
                    WHERE time >= now() - interval '24 hours';"""
                     )

        # Fetch the result
        result = curs.fetchall()

        if result:
            print(result)
        else:
            print("No result found")
    finally:
        # Close the cursor and connection
        curs.close()
        conn.close()

        return result;

# Input city and country
# Returns uri of top recommended song of that location of the past 24 hours
def top_songs(city, country):
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
        # Execute the SQL query
        print("Executing SQL query...")
        curs.execute("""SELECT DISTINCT uri, title, city, country, 
                    COUNT(uri) OVER (PARTITION BY uri, city, country) AS frequency
                    FROM spotify JOIN (SELECT DISTINCT * FROM location) AS locate
                    ON spotify.ipaddress = locate.ipaddress
                    WHERE time >= now() - interval '24 hours' AND city = %s AND country = %s
                    ORDER BY frequency DESC;""",
                    (city, country)
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

# Returns total number of recommendations made by app.
def total_recommendations(city, country):
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
        # Execute the SQL query
        print("Executing SQL query...")
        curs.execute("""SELECT COUNT(*)
                    FROM spotify;"""
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

# Returns
def city_valency_mood(city, country):
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
        # Execute the SQL query
        print("Executing SQL query...")
        curs.execute("""SELECT COUNT(*)
                    FROM spotify;"""
                     )

        SELECT
        DISTINCT
        city, country, mood, COUNT(mood)
        OVER(PARTITION
        BY
        city, country, mood), ROUND(AVG(valency * 1.0)
        OVER(PARTITION
        BY
        city, country), 1) AS
        average_val
        FROM
        mood
        JOIN
        location
        ON
        location.ipaddress = mood.ipaddress
        ORDER
        BY
        average_val
        DESC;

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

mood_data = {
    "London": {"mood": "Happy", "song": "Here Comes the Sun", "index": 0.2},
    "New York": {"mood": "Energetic", "song": "Here Comes the Sun", "index": 0.8},
    "California": {"mood": "Energetic", "song": "Here Comes the Sun", "index": 0.5},
    "Berlin": {"mood": "Energetic", "song": "Here Comes the Sun", "index": 0.4},
    "Beijing": {"mood": "Energetic", "song": "Here Comes the Sun", "index": 0.3}
}





