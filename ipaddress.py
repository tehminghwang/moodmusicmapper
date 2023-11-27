from flask import Flask, render_template, request
import requests
app = Flask(__name__)


@app.route('/')
def get_city_from_ip():

    ip_address = request.headers.get('x-real-ip') or request.headers.get('x-forwarded-for', request.remote_addr)
    access_key = 'c35f452278b88715ee4c2190eba7d401'
    url = f"http://api.ipstack.com/{ip_address}?access_key={access_key}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if 'city' in data:
            return data['city']
        else:
            return "City information not found for this IP address"

    except requests.RequestException as e:
        return f"Error: {e}"
