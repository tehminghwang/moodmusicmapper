from flask import Flask, render_template, request
import openai
import os
app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")
#client = openai.Client()

@app.route("/")
def hello_world():
    return render_template("index.html")

def send_request(mood):
    try:
        response = openai.Completion.create(
            engine="text-davinci-004",
            prompt=f"ONLY generate values for valency, danceability, and energy based on the mood: {mood}",
            max_tokens=60
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

@app.route("/submit", methods=["POST"])
def submit():
    input_mood = request.form.get("mood")
    reply = send_request(input_mood)
    return render_template("mood.html", mood=reply)

if __name__ == "__main__":
    app.run(debug=True)