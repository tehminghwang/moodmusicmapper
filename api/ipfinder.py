from flask import request
import requests
import os

def get_city_from_ip(ref city, ref country, ref ip_address):

    ip_address = request.headers.get('x-real-ip') or request.headers.get('x-forwarded-for', request.remote_addr)
    #access_key = "c35f452278b88715ee4c2190eba7d401"
    access_key = os.environ.get('IP_KEY')

    #url = f"http://api.ipstack.com/2a0c:5bc0:40:11c4:631c:ac68:22c6:440?access_key={access_key}"
    url = f"http://api.ipstack.com/{ip_address}?access_key={access_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if 'city' in data:
            city = data['city']
        if 'country' in data:
            country = data['country']
        return
            #return city
        #else:
            #return "City information not found for this IP address"

    except requests.RequestException as e:
        return f"Error: {e}"
