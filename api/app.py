from flask import Flask, render_template, request#, re
from openai import OpenAI
import os
app = Flask(__name__)


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
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
                 'content': f'I am feeling {mood}. Can you suggest music characteristics like valency (value from 0.0 to 1.0 with 1.0 being more positive (e.g. happy, cheerful, euphoric)), danceability (value of 0.0 is least danceable and 1.0 is most danceable based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity), and energy (from 0.0 to 1.0 and represents a perceptual measure of intensity and activity) that would suit my mood, and describe my mood in 1 word? Reply only with three values and a word.'}
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
    return render_template("mood.html", mood=reply)

if __name__ == "__main__":
    app.run(debug=True)