from flask import Flask, render_template, request
from openai import OpenAI
import os
import re
#from api import spotify_mod, database, ipfinder
import spotify_mod, database, ipfinder
app = Flask(__name__)


client = OpenAI(
    #api_key="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"
    api_key=os.environ.get('OPENAI_API_KEY')
    #api_key=os.environ.get("API_URL")
)

@app.route("/")
def hello_world():
    return render_template("index.html")

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
        #result = re.findall(r"[-+]?\d*\.\d+|\d+", last_message)
        #valency = result[0]
        #dance = result[1]
        #energy = result[2]

        # finding the index of last space
        #index = string.rfind(" ")
        #summary = string[index + 1:]
        return last_message #+ str(valency) + str(dance) + str(energy) + summary
        #return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

@app.route("/submit", methods=["POST"])
def submit():
    input_mood = request.form.get("mood")
    reply = send_request(input_mood)
    valency, danceability, energy, mood, song, singer = extract_values(reply)
    response = f"Valency: {valency}, Danceability: {danceability}, Energy: {energy}, Mood: {mood}, Song: {song}, Singer: {singer}"
    playlist = spotify_mod.spotify_main(valency, danceability, energy)
    city = ipfinder.get_city_from_ip()
    #country=time=cookies = "123abc" # temp placeholder
    #insert_into_database(cookies, valency, danceability, energy, mood, time, ipaddress, city, country)
    return render_template("mood.html", input_mood = input_mood, mood=playlist, response=response, reply=reply, city=city)

if __name__ == "__main__":
    app.run(debug=True)

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