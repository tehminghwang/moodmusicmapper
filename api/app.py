from flask import Flask, render_template, request
from openai import OpenAI
import os
app = Flask(__name__)


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    #api_key=os.environ.get("OPENAI_API_KEY")
    api_key= "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"
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
                 'content': f'I am feeling {mood}. Can you suggest music characteristics like valency, danceability, and energy that would suit my mood?'}
            ],
            max_tokens=60
        )
        last_message = response.choices[0].message.content
        return last_message
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