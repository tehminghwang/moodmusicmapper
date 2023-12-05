import os
from dotenv import load_dotenv
import spotify_mod

client_id = 'e7f726d8be8f4c49820046043edc2e79'

if os.getenv("VERCEL"):
# Load environment variables from Vercel secrets
    client_secret = os.environ.get('SPOTIFY_KEY')
elif os.getenv("GIT_SPOTIFY"):
    client_secret = os.environ.get('GIT_SPOTIFY')
else:
# Load environment variables from the .env file
    load_dotenv()
    client_secret= os.environ.get("SPOTIFY")


"""
# test if access token if retrieved
def test_access_token():
    
    access_token = spotify_mod.get_spotify_access_token(client_id, client_secret)

    assert access_token != None


# test if a list of songs is called
def test_spotify_recommendations():
    recommend_songs = spotify_mod.spotify_main(0.5, 0.5, 0.5, 'pop',['Slow Hands Niall Horan', 'Words Low'])

    true_test = True
    for song in recommend_songs:
        true_test *= all(song.values())  # Test if all items in the song have a value
        # If any item is NoneType, true_test will be set to 0

    assert len(recommend_songs) == 12 and true_test

"""
# commented out to avoid frequent spotify API calls


# test if a song id is called
def test_artist_top_song():

    song_id = spotify_mod.get_artist_top_song('1Hsdzj7Dlq2I7tHP7501T4','GB')

    assert song_id != None





