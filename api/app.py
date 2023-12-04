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
            
            #model='gpt-3.5-turbo',
            #messages=[
            #    {'role': 'system', 'content': 'You are a helpful assistant.'},
            #    {'role': 'user',
            #     'content': f'I am feeling {mood}. Can you suggest music characteristics like valency (value from 0.0 to 1.0 with 1.0 being more positive (e.g. happy, cheerful, euphoric)), danceability (value of 0.0 is least danceable and 1.0 is most danceable based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity), and energy (from 0.0 to 1.0 and represents a perceptual measure of intensity and activity) that would suit my mood, and describe my mood in 1 word, and recommend 1 song to suit my mood? Reply as [Valency: ??] [Danceability: ??] [Energy: ??] [Mood: ??] [Song: ??] [Singer: ??].'}
            #],
            #max_tokens=60
            
            #model="ft:gpt-3.5-turbo-0613:personal::8R0aC6w3",
            #messages=[
            #{"role": "system", "content": "Assistant to identify valency, energy and danceability index (for song selection) based on description of user's narrative of their sentiment, mood, context, description, feelings, or events. The recommendations should be congruent to the user's current state, and tailored to the emotional tone and energy level described by the user."},
            #{"role": "user", "content": f'i feel {mood} now'}

            model="ft:gpt-3.5-turbo-0613:personal::8S0F2gyx",
            messages=[
            {"role": "system", "content": "Assistant to recommend valency(songs with high valence sound more positive e.g. Happy, cheerful, euphoric)(0.0 to 1.0), energy(energetic tracks feel fast, loud, and noisy)(0.0 to 1.0), danceability(suitable for dancing based on musical elements including tempo, rhythm stability, beat strength)(0.0 to 1.0) and 3 recommended songs that resonates with a description of user's narrative of their sentiment, mood, context, description, feelings, or events."},
            {"role": "user", "content": f'{mood}'}
            ]
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
                <br>
                <iframe src="https://open.spotify.com/embed/track/6kex4EBAj0WHXDKZMEJaaF" width="250" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                <br>
                <div class = "share">  
			        <div class = "shareto">
			            <a href="https://www.facebook.com/sharer/sharer.php?quote=Mood Music Mapper recommended me to listen to this!\n\nGet your recommendation:\nhttps://moodmusicmapper.vercel.app/\n&u=https://open.spotify.com/track/6kex4EBAj0WHXDKZMEJaaF" 
				        target="_blank" class="facebook-button">
				            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30" width="30px" height="30px">    
					            <path d="M15,3C8.373,3,3,8.373,3,15c0,6.016,4.432,10.984,10.206,11.852V18.18h-2.969v-3.154h2.969v-2.099c0-3.475,1.693-5,4.581-5 c1.383,0,2.115,0.103,2.461,0.149v2.753h-1.97c-1.226,0-1.654,1.163-1.654,2.473v1.724h3.593L19.73,18.18h-3.106v8.697 C22.481,26.083,27,21.075,27,15C27,8.373,21.627,3,15,3z"/>
				            </svg>
			            </a>
			            <a href="https://twitter.com/intent/tweet?text=Mood Music Mapper recommended me to listen to this!%0A%0AGet your recommendation:%0Ahttps://moodmusicmapper.vercel.app/%0A%0A&url=https://open.spotify.com/track/6kex4EBAj0WHXDKZMEJaaF" 
				        target="_blank" id = "twitter_x-button"> 
				            <svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 30 30" width="30px" height="30px">
					            <path d="M26.37,26l-8.795-12.822l0.015,0.012L25.52,4h-2.65l-6.46,7.48L11.28,4H4.33l8.211,11.971L12.54,15.97L3.88,26h2.65 l7.182-8.322L19.42,26H26.37z M10.23,6l12.34,18h-2.1L8.12,6H10.23z"/>
				            </svg>
			            </a>
			        </div>
			    </div>
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

    if request.cookies.get('ipaddress') is not None:
        print("IP address in Cookie")
        return redirect(url_for("loading_page", input_mood=input_mood))
    else:
        ipaddress = ipfinder.get_ip()
        response = make_response(redirect(url_for("loading_page", input_mood=input_mood)))
        response.set_cookie('ipaddress', ipaddress, max_age=60 * 60 * 24 * 30)
        location_info = ipfinder.get_location_from_ip(ipaddress)
        if location_info['city'] is not None:
            city = location_info['city']
            country = location_info['country']
            database.location_into_table(ipaddress, city, country)
            response.set_cookie('city', city, max_age=60 * 60 * 24 * 30)  # Cookie expires in 30 days

    # Simulate a delay (2 seconds) to simulate a background task
    #time.sleep(2)
    # Redirect to the loading page before going to the response page
    return response


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
        valency, danceability, energy, mood, genre, song1, singer1, song2, singer2, song3, singer3 = extract_values(reply)
        print(genre)
        response = f"Valency: {valency}, Danceability: {danceability}, Energy: {energy}, Mood: {mood}"
        song_list = [song1 + " " + singer1, song2 + " " + singer2, song3 + " " + singer3]
        print(song_list)
        playlist = spotify_mod.spotify_main(valency, danceability, energy, genre, song_list)
        print(playlist)
        playlist_json = json.dumps(playlist)
        #response.set_cookie('playlist', playlist, max_age=60 * 60 * 24 * 30)  # Cookie expires in 30 days

        song_of_day = database.song_of_day()
        #singer_of_day = database.getysinger_of_day()
        #singer_of_day_top_song = spotify_mod.search_artist_top_song(singer_of_day)
        singer_of_day_top_song = None
    
        ipaddress = request.cookies.get('ipaddress')
        print(ipaddress)
        input_mood = input_mood.replace("%20", " ")
        print(input_mood)
        database.mood_into_table(ipaddress, input_mood, mood, valency, danceability, energy, playlist)

        # Generate the map with mood data
        folium_map = create_map(mood_data)
        map_html = folium_map._repr_html_()

        #country=time=cookies = "123abc" # temp placeholder
        #insert_into_database(cookies, valency, danceability, energy, mood, time, ipaddress, city, country)
        city = request.cookies.get('city')
        if city == None:
            city = "your area"

        response_html = render_template("mood.html", input_mood = input_mood, mood=playlist, response=response, reply=reply, 
                                        city=city, map_html=map_html, song_of_day=song_of_day, singer_of_day_top_song=singer_of_day_top_song)
        # Create a response object from the rendered HTML
        response = make_response(response_html)
        # Set a cookie in the response object
        response.set_cookie('playlist', playlist_json, max_age=60 * 60 * 24 * 30)  # Cookie expires in 30 days

    
    except Exception as e:
        print("Error", e)
        response = error_page()

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
    #genre_pattern = r"Genre:\s([^\]]+)"
    genre_pattern = r"Genre:\s(\w+)(?!.*Genre:)"
    song_pattern = r"Song\d+:\s([^\]]+)"
    singer_pattern = r"Singer\d+:\s([^\]]+)"

    # Extracting values
    valency = re.search(valency_pattern, text)
    danceability = re.search(danceability_pattern, text)
    energy = re.search(energy_pattern, text)
    mood = re.search(mood_pattern, text)
    genre = re.search(genre_pattern, text)
    song1 = re.search(song_pattern.replace('\d+', '1'), text)
    singer1 = re.search(singer_pattern.replace('\d+', '1'), text)
    song2 = re.search(song_pattern.replace('\d+', '2'), text)
    singer2 = re.search(singer_pattern.replace('\d+', '2'), text)
    song3 = re.search(song_pattern.replace('\d+', '3'), text)
    singer3 = re.search(singer_pattern.replace('\d+', '3'), text)

    # Assigning to variables and converting to appropriate types
    valency = float(valency.group(1)) if valency else None
    danceability = float(danceability.group(1)) if danceability else None
    energy = float(energy.group(1)) if energy else None
    mood = mood.group(1) if mood else None
    genre = genre.group(1) if genre else None
    song1 = song1.group(1) if song1 else None
    singer1 = singer1.group(1) if singer1 else None
    song2 = song2.group(1) if song2 else None
    singer2 = singer2.group(1) if singer2 else None
    song3 = song3.group(1) if song3 else None
    singer3 = singer3.group(1) if singer3 else None


    return valency, danceability, energy, mood, genre, song1, singer1, song2, singer2, song3, singer3



#"handler": "app.app",
#"runtime": "python3.8",