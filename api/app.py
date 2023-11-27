from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_mood = "ONLY generate values for valency, danceability and enegery based on the mood: " + request.form.get("mood")
    reply = send_request(input_mood)
    return render_template("mood.html", mood=reply)


def send_request(prompt):
    api_key = "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"  # Replace with your OpenAI API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4.0-turbo",  # or another model version
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post("https://api.openai.com/v1/engines/gpt-4.0-turbo/completions", json=payload, headers=headers)
    return response.json()

