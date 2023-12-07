import psycopg2 as db
import configparser
from dotenv import load_dotenv
import os


def setUp():
    # Use a separate testing database or create a temporary schema for testing
    config = configparser.ConfigParser()
    config.read("dbtool.ini")

    if os.getenv("VERCEL"):
        # Load environment variables from Vercel secrets
        password = os.environ.get("DATABASE_KEY")
    elif os.getenv("GIT_DATABASE"):
        password = os.environ.get("GIT_DATABASE")
    else:
        # Load environment variables from the .env file
        load_dotenv()
        password = os.environ.get("DATABASE")

    config["connection"]["password"] = password

    conn = db.connect(**config["connection"])
    curs = conn.cursor()
    return conn, curs

# Inserts location data from this session into database.
def location_into_table(conn, curs, ipaddress, city, country, country_code):
    print("Executing SQL query...")
    curs.execute(
        """INSERT INTO location VALUES (%s, %s, %s, %s);""",
        (ipaddress, city, country, country_code),
    )
    print("Committing transaction...")
    conn.commit()


# Inserts user input and OpenAI output into database.
def mood_into_table(
    conn, curs, ipaddress, input_mood, mood, valency, danceability, energy, playlist
):
    print("Executing SQL query...")
    curs.execute(
        """INSERT INTO mood VALUES (NOW(), %s, %s, %s, %s, %s, %s);""",
        (ipaddress, input_mood, mood, valency, danceability, energy),
    )

    for item in playlist:
        curs.execute(
            """INSERT INTO spotify VALUES (NOW(), %s, %s, %s, %s, %s);""",
            (
                ipaddress,
                item["name"],
                item["artist"],
                item["uri"],
                item["artist_uri"],
            ),
        )

    print("Committing transaction...")
    conn.commit()

# Returns URI of top recommended song of past 24 hours.
def song_of_day(curs):
    # Execute the SQL query
    print("Executing SQL query...")
    curs.execute(
        """SELECT DISTINCT uri, title, artist, COUNT(uri) OVER (PARTITION BY uri) AS frequency 
                FROM spotify 
                WHERE time >= now() - interval '24 hours' 
                ORDER BY frequency DESC LIMIT 1;"""
    )

    # Fetch the result
    song = curs.fetchone()

    if song:
        print(song)
    else:
        print("No result found")

    return song[0]


# Returns all cities (and corresponding country) that have used the app in the past 24 hours.
def city_clients(curs):
    # Execute the SQL query
    print("Executing SQL query...")
    curs.execute(
        """SELECT DISTINCT city, country
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

    return result


# Returns info specific to city and country
def city_country_info(curs, city, country):
    # Dictionary for all data to be returned together.
    city_info = dict()

    # Execute the SQL query
    print("Executing SQL query...")
    # This query finds top song of past 24 hours by city and country
    curs.execute(
        """SELECT DISTINCT uri, title, city, country, 
                COUNT(uri) OVER (PARTITION BY uri, city, country) AS frequency
                FROM spotify JOIN (SELECT DISTINCT * FROM location) AS locate
                ON spotify.ipaddress = locate.ipaddress
                WHERE time >= now() - interval '24 hours' AND city = %s AND country = %s
                ORDER BY frequency DESC;""",
        (city, country),
    )

    # Fetch the result
    top_song = curs.fetchone()

    if top_song:
        print(top_song)
        city_info["song"] = top_song[0]
    else:
        print("No song result found")

    # Execute the SQL query
    print("Executing SQL query...")
    # This query finds top mood of past 24 hours by city and country
    curs.execute(
        """SELECT DISTINCT mood, COUNT(mood) AS frequency, city, country
                FROM mood JOIN (SELECT DISTINCT * FROM location) AS locate 
                ON mood.ipaddress = locate.ipaddress
                WHERE time >= now() - interval '24 hours' AND city = %s AND country = %s
                GROUP BY city, country, mood ORDER BY frequency DESC;""",
        (city, country),
    )

    # Fetch the result
    mood = curs.fetchone()

    if mood:
        print(mood)
        city_info["mood"] = mood[0]
    else:
        print("No mood result found")

    # Execute the SQL query
    print("Executing SQL query...")
    # This query finds top artist of past 24 hours by city and country
    curs.execute(
        """SELECT DISTINCT artist_uri, artist, COUNT(artist_uri) AS frequency, city, country
                FROM spotify JOIN (SELECT DISTINCT * FROM location) AS locate 
                ON spotify.ipaddress = locate.ipaddress
                WHERE time >= now() - interval '24 hours' AND city = %s AND country = %s
                GROUP BY city, country, artist_uri, artist ORDER BY frequency DESC;""",
        (city, country),
    )

    # Fetch the result
    artist = curs.fetchone()

    if artist:
        print(mood)
        city_info["artist"] = artist[0]
    else:
        print("No artist result found")

    # Execute the SQL query
    print("Executing SQL query...")
    # This query finds average valency of past 24 hours by city and country
    curs.execute(
        """SELECT DISTINCT ROUND(AVG(valency*1.0),1) AS average, city, country
                FROM mood JOIN (SELECT DISTINCT * FROM location) AS locate 
                ON mood.ipaddress = locate.ipaddress
                WHERE time >= now() - interval '24 hours' AND city = %s AND country = %s
                GROUP BY city, country;""",
        (city, country),
    )

    # Fetch the result
    valency = curs.fetchone()

    if valency:
        print(valency)
        city_info["valency"] = valency[0]
    else:
        print("No artist result found")

    print(city_info)
    return city_info


# Returns total number of recommendations made by app.
# Should be used by landing page
def total_recommendations(curs):
    # Execute the SQL query
    print("Executing SQL query...")
    curs.execute(
        """SELECT COUNT(*)
                FROM spotify;"""
    )

    # Fetch the result
    result = curs.fetchone()

    if result:
        print(result)
    else:
        print("No result found")

    return result[0]


# Returns uri of top recommended artist of past 24 hours
def artist_of_day(curs):
    # Execute the SQL query
    print("Executing SQL query...")
    curs.execute(
        """SELECT DISTINCT artist_uri, artist, COUNT(artist) AS frequency
                FROM spotify 
                WHERE time >= now() - interval '24 hours'
                GROUP BY artist, artist_uri
                ORDER BY frequency DESC LIMIT 1;"""
    )

    # Fetch the result
    result = curs.fetchone()

    if result:
        print("Artist", result)
    else:
        print("No result found")

    return result[0]


# Display phrases that match valency on response page
def display_phrase(curs, scale, integer):
    # Execute the SQL query
    print("Executing SQL query...")
    curs.execute(
        """SELECT phrase
                FROM valency
                WHERE valence = %s;""",
        (scale,),
    )

    # Fetch the result
    result = curs.fetchall()

    if result:
        print(result)
    else:
        print("No result found")

    text_only = [item[0] for item in result]

    return text_only[integer]

def tearDown(conn, curs):
    curs.close()
    conn.close()
