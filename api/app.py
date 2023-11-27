from flask import Flask, render_template, request
import openai
import os
import requests
app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")
client = openai.Client()

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_mood = "ONLY generate values for valency, danceability and enegery based on the mood: " + request.form.get("mood")
    reply = send_request(input_mood)
    return render_template("mood.html", mood=reply)


def send_request(prompt):
    response = client.Completion.create(
        model="text-davinci-003",  # Replace with your desired model
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )
    return response


