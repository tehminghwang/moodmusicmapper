import requests

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

def get_spotify_recommendations(access_token, valence, danceability, energy):
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
    print(response)
    recommendations = response.json()['tracks']

    # Extract relevant information from recommendations
    tracks = []
    for track in recommendations:
        track_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'uri': track['uri']
        }
        tracks.append(track_info)

    return tracks

#if __name__ == "__main__":
    # Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual Spotify API credentials
    client_id = 'bc4a63dca78b417db515f5b70813b986'
    client_secret = 'd5cc981f4fc84e0d82aea910397645df'

    access_token = get_spotify_access_token(client_id, client_secret)

    # Replace these values with the desired input parameters
    seed_genre = 'pop' #seed artist, genres, tracks: at least one required
    valence = 0.8  # Range: 0.0 to 1.0
    danceability = 0.7  # Range: 0.0 to 1.0
    energy = 0.8  # Range: 0.0 to 1.0

    recommendations = get_spotify_recommendations(access_token, valence, danceability, energy)

    # Print the recommendations
    for i, track in enumerate(recommendations, start=1):
        print(f"{i}. {track['name']} by {track['artist']} (URI: {track['uri']})")
