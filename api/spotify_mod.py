import requests
import os
from dotenv import load_dotenv
from flask import current_app

def get_spotify_access_token(client_id, client_secret):
    # Get Spotify access token using client credentials flow
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(auth_url, data=auth_data)
    access_token = response.json().get('access_token')

    print(access_token)

    return access_token

def get_spotify_recommendations(access_token, seed_genre, valence, danceability, energy):
    # Get recommendations based on input parameters
    recommendations_url = 'https://api.spotify.com/v1/recommendations'
    headers = {'Authorization': f'Bearer {access_token}'}
    print(seed_genre)
    print(valence)
    print(danceability)
    print(energy)
    params = {
        'limit': 10,  # Number of recommendations to retrieve
        'seed_genres': seed_genre,
        'target_valence': valence,
        'target_danceability': danceability,
        'target_energy': energy
    }

    response = requests.get(recommendations_url, headers=headers, params=params)
    print(response)
    recommendations = response.json()['tracks']

    # Extract relevant information from recommendations
    tracks = []
    for track in recommendations:
        track_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'uri': track['uri'].partition("spotify:track:")[2],
            'artist_uri': track['artists'][0]['id']
        }
        tracks.append(track_info)

    return tracks

def spotify_main(valence, danceability, energy, genre, song_list):    # Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual Spotify API credentials
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

    access_token = get_spotify_access_token(client_id, client_secret)

    if is_genre_available(genre):
        print(f"{genre} is available on Spotify.")
        seed_genre = genre
    else:
        print(f"{genre} is not available on Spotify.")
        seed_genre = "pop"

    #available_genres = get_spotify_genres(access_token)

    # Replace these values with the desired input parameters
    # seed_genre = genre if genre in available_genres else "pop" #seed artist, genres, tracks: at least one required
    #valence = 0.8  # Range: 0.0 to 1.0
    #danceability = 0.7  # Range: 0.0 to 1.0
    #energy = 0.8  # Range: 0.0 to 1.0
    recommendations = get_spotify_recommendations(access_token, seed_genre, valence, danceability, energy)

    search_result = search_spotify_song(song_list, access_token)

    playlist = search_result + recommendations

    return playlist

    # Print the recommendations
    #for i, track in enumerate(recommendations, start=1):
        #print(f"{i}. {track['name']} by {track['artist']} (URI: {track['uri']})")

# def get_spotify_genres(access_token):
#
#     # Get list of genres
#     base_url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
#     headers = {'Authorization': f'Bearer {access_token}'}
#     genres_response = requests.get(base_url, headers=headers)
#     genres_data = genres_response.json()
#
#     # Extract genre names
#     genres = genres_data['genres']
#
#     return genres


def is_genre_available(target_genre):

    available_genres = ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "bluegrass", "blues", 
                        "bossanova", "brazil", "breakbeat", "british", "cantopop", "chicago-house", "children", "chill", "classical", 
                        "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco", "disney", 
                        "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", "french", "funk", "garage", 
                        "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle", 
                        "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial", 
                        "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", 
                        "metal", "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age", "new-release", "opera", "pagode", 
                        "party", "philippines-opm", "piano", "pop", "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", 
                        "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", 
                        "romance", "sad", "salsa", "samba", "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", 
                        "soul", "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop", 
                        "turkish", "work-out", "world-music"]

        # Check if the target genre is in the list
    if target_genre in available_genres:
        return True
    else:
        return False
    

def search_spotify_song(query_list, access_token):
    base_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}

    # Specify the type as 'track' for searching songs
    song_list = []

    for query in query_list:    
        params = {'q': query, 'type': 'track'}

        response = requests.get(base_url, headers=headers, params=params)
        search_results = response.json()

        # Check if there are tracks in the search results
        if 'tracks' in search_results:
            tracks = search_results['tracks']['items']

            if tracks:
                # Extract information about the first track in the search results
                first_track = tracks[0]
                track_info = {
                'name': first_track['name'],
                'artist': first_track['artists'][0]['name'],
                'uri': first_track['id'],
                'artist_uri': first_track['artists'][0]['id']
                }
                
                song_list.append(track_info)
    return song_list

def get_artist_top_song(singer_id, country):
    
    client_id = 'e7f726d8be8f4c49820046043edc2e79'

    if os.getenv("VERCEL"):
    # Load environment variables from Vercel secrets
        client_secret = os.environ.get('SPOTIFY_KEY')
    else:
    # Load environment variables from the .env file
        load_dotenv()
        client_secret= os.environ.get("SPOTIFY")

    access_token = get_spotify_access_token(client_id, client_secret)
    
    if country == None:
        country = 'GB'

    base_url = f'https://api.spotify.com/v1/artists/{singer_id}/top-tracks'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'market': country  # required
    }

    response = requests.get(base_url, headers=headers, params=params)
    search_results = response.json()
    
    song_id = None

    # Check if there are tracks in the search results
    if 'tracks' in search_results:
        # Extract information about the first track in the search results
        first_song = search_results['tracks'][0]
        song_id = first_song['id']
    
    return song_id

