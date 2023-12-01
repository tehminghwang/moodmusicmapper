from flask import Flask, render_template, request, redirect, url_for, make_response, current_app
from dotenv import load_dotenv
from openai import OpenAI
import os
import re
import folium
import json
import time
from branca.colormap import LinearColormap
if os.getenv("VERCEL"):
    from api import spotify_mod, database, ipfinder
else:
    import spotify_mod, database, ipfinder
import geopy
from geopy.geocoders import Nominatim
app = Flask(__name__)

# Check if running on Vercel
if os.getenv("VERCEL"):
    # Load environment variables from Vercel secrets
    open_ai_key=os.environ.get('OPENAI_API_KEY')
else:
    # Load environment variables from the .env file
    load_dotenv()
    open_ai_key= os.environ.get("OPEN_AI")



client = OpenAI(
    api_key = open_ai_key
)

@app.route("/")
def hello_world():
    playlist_cookie = request.cookies.get('playlist')
    saved_playlist = None  # Initialize saved_playlist to None
    if playlist_cookie:
        try:
            saved_playlist = json.loads(playlist_cookie)
        except json.JSONDecodeError:
            # Handle the case where the cookie contains invalid JSON
            pass

    return render_template("index.html", mood=saved_playlist)

def send_request(mood):
    try:
        response = client.chat.completions.create(
            #engine="gpt-4",
            #prompt=f"ONLY generate values for valency, danceability, and energy based on the mood: {mood}",
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user',
                 'content': f'I am feeling {mood}. Can you suggest music characteristics like valency (value from 0.0 to 1.0 with 1.0 being more positive (e.g. happy, cheerful, euphoric)), danceability (value of 0.0 is least danceable and 1.0 is most danceable based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity), and energy (from 0.0 to 1.0 and represents a perceptual measure of intensity and activity) that would suit my mood, and describe my mood in 1 word, and recommend 1 song to suit my mood? Reply as [Valency: ??] [Danceability: ??] [Energy: ??] [Mood: ??] [Song: ??] [Singer: ??].'}
            ],
            max_tokens=60
        )
        last_message = response.choices[0].message.content


        return last_message
        #return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Placeholder for mood data
mood_data = {
    "London": {"mood": "Happy", "song": "Here Comes the Sun", "index": 0.2},
    "New York": {"mood": "Energetic", "song": "Here Comes the Sun", "index": 0.8},
    "California": {"mood": "Energetic", "song": "Here Comes the Sun", "index": 0.5},
    "Berlin": {"mood": "Energetic", "song": "Here Comes the Sun", "index": 0.4},
    "Beijing": {"mood": "Energetic", "song": "Here Comes the Sun", "index": 0.3}
}

def create_colormap():
    colors = ['green', 'yellow', 'red']
    index = [0, 0.5, 1]  # Points at which colors change
    return LinearColormap(colors, vmin=min(index), vmax=max(index))


def create_map(mood_data):
    # Start with a world map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Define a linear color map
    colormap = create_colormap()

    for city, info in mood_data.items():
        lat, lon = get_coordinates(city)
        if lat is not None and lon is not None:
            # Get color from the colormap
            color = colormap(info['index'])

            # Customize the popup with HTML content
            html_content = f"""
            <div style="width: 250px; height: 150px;">
                <strong>{city}</strong><br>
                Mood: {info['mood']}<br>
                Song: {info['song']}<br>
                <iframe src="https://open.spotify.com/embed/track/6kex4EBAj0WHXDKZMEJaaF" width="250" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
            </div>
            """
            iframe = folium.IFrame(html_content, width=270, height=200)
            popup = folium.Popup(iframe, parse_html=False)

            # Add a Circle marker with the color
            folium.Circle(
                location=[lat, lon],
                radius=300000,  # Adjust the radius as needed
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=1,
                popup=popup
            ).add_to(m)

    # Optionally, add the colormap to the map for reference
    colormap.add_to(m)

    return m




@app.route("/submit", methods=["POST"])
def submit():
    input_mood = request.form.get("mood")

    # Simulate a delay (2 seconds) to simulate a background task
    #time.sleep(2)

    # Redirect to the loading page before going to the response page
    return redirect(url_for("loading_page", input_mood=input_mood))


@app.route("/loading/<input_mood>")
def loading_page(input_mood):
    # Render the loading page

    return render_template("loading.html", input_mood=input_mood)


@app.route("/response/<input_mood>")
def response_page(input_mood):

    try:
        # Process the request and prepare the response here
        # You can use the 'input_mood' parameter to generate the response
        print("Hello, World!")
        reply = send_request(input_mood)
        valency, danceability, energy, mood, song, singer = extract_values(reply)
        response = f"Valency: {valency}, Danceability: {danceability}, Energy: {energy}, Mood: {mood}, Song: {song}, Singer: {singer}"
        playlist = spotify_mod.spotify_main(valency, danceability, energy)
        playlist_json = json.dumps(playlist)
        #response.set_cookie('playlist', playlist, max_age=60 * 60 * 24 * 30)  # Cookie expires in 30 days

        ipaddress = ipfinder.get_ip()
        location_info = ipfinder.get_location_from_ip(ipaddress)
        city = location_info['city']
        country = location_info['country']

        database.insert_into_table(ipaddress, input_mood, mood, valency, danceability, energy, city, country, playlist)

        # Generate the map with mood data
        folium_map = create_map(mood_data)
        map_html = folium_map._repr_html_()

        #country=time=cookies = "123abc" # temp placeholder
        #insert_into_database(cookies, valency, danceability, energy, mood, time, ipaddress, city, country)
        response_html = render_template("mood.html", input_mood = input_mood, mood=playlist, response=response, reply=reply, city=city, map_html=map_html)
        # Create a response object from the rendered HTML
        response = make_response(response_html)
        # Set a cookie in the response object
        response.set_cookie('playlist', playlist_json, max_age=60 * 60 * 24 * 30)  # Cookie expires in 30 days

        return response
    
    except Exception:
        response = error_page

    return response

@app.route("/error")
def error_page():
    
    return render_template("error.html")
    


if __name__ == "__main__":
    app.run(debug=True)



def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="moodmusicmapper")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def extract_values(text):
    # Regular expressions to extract the values
    valency_pattern = r"Valency:\s([0-9.]+)"
    danceability_pattern = r"Danceability:\s([0-9.]+)"
    energy_pattern = r"Energy:\s([0-9.]+)"
    mood_pattern = r"Mood:\s(\w+)(?!.*Mood:)"
    song_pattern = r"Song:\s\"([^\"]+)\""
    singer_pattern = r"Singer:\s([^\]]+)"

    # Extracting values
    valency = re.search(valency_pattern, text)
    danceability = re.search(danceability_pattern, text)
    energy = re.search(energy_pattern, text)
    mood = re.search(mood_pattern, text)
    song = re.search(song_pattern, text)
    singer = re.search(singer_pattern, text)

    # Assigning to variables and converting to appropriate types
    valency = float(valency.group(1)) if valency else None
    danceability = float(danceability.group(1)) if danceability else None
    energy = float(energy.group(1)) if energy else None
    mood = mood.group(1) if mood else None
    song = song.group(1) if song else None
    singer = singer.group(1) if singer else None

    return valency, danceability, energy, mood, song, singer



#"handler": "app.app",
#"runtime": "python3.8",
