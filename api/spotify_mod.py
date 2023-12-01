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
    return access_token

def get_spotify_recommendations(access_token, seed_genre, valence, danceability, energy):
    # Get recommendations based on input parameters
    recommendations_url = 'https://api.spotify.com/v1/recommendations'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'limit': 10,  # Number of recommendations to retrieve
        'seed_genres': seed_genre,
        'target_valence': valence,
        'target_danceability': danceability,
        'target_energy': energy
    }

    response = requests.get(recommendations_url, headers=headers, params=params)
    
    recommendations = response.json()['tracks']

    # Extract relevant information from recommendations
    tracks = []
    for track in recommendations:
        track_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'uri': track['uri'].partition("spotify:track:")[2]
        }
        tracks.append(track_info)

    return tracks

def spotify_main(valence, danceability, energy, genre):    # Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual Spotify API credentials
    client_id = 'e7f726d8be8f4c49820046043edc2e79'

    if os.getenv("VERCEL"):
    # Load environment variables from Vercel secrets
        client_secret = os.environ.get('SPOTIFY_KEY')
    else:
    # Load environment variables from the .env file
        load_dotenv()
        client_secret= os.environ.get("SPOTIFY")

    access_token = get_spotify_access_token(client_id, client_secret)

    available_genres = get_spotify_genres(access_token)

    # Replace these values with the desired input parameters
    seed_genre = genre if genre in available_genres else "pop" #seed artist, genres, tracks: at least one required
    #valence = 0.8  # Range: 0.0 to 1.0
    #danceability = 0.7  # Range: 0.0 to 1.0
    #energy = 0.8  # Range: 0.0 to 1.0
    recommendations = get_spotify_recommendations(access_token, seed_genre, valence, danceability, energy)

    print(recommendations)

    return recommendations

    # Print the recommendations
    #for i, track in enumerate(recommendations, start=1):
        #print(f"{i}. {track['name']} by {track['artist']} (URI: {track['uri']})")

client_id = 'e7f726d8be8f4c49820046043edc2e79'

def get_spotify_genres(access_token):

    # Get list of genres
    base_url = 'https://api.spotify.com/v1/browse/categories'
    headers = {'Authorization': f'Bearer {access_token}'}
    genres_response = requests.get(base_url, headers=headers)
    genres_data = genres_response.json()

    # Extract genre names
    genres = [category['name'] for category in genres_data['categories']['items']]
    
    return genres


def search_spotify_song(query, access_token):
    base_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}

    # Specify the type as 'track' for searching songs
    params = {'q': query, 'type': 'track'}

    response = requests.get(base_url, headers=headers, params=params)
    search_results = response.json()

    id = None

    # Check if there are tracks in the search results
    if 'tracks' in search_results:
        tracks = search_results['tracks']['items']

        if tracks:
            # Extract information about the first track in the search results
            first_track = tracks[0]
            id = first_track['id']
    
    return id

