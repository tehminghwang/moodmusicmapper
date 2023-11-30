from flask import request, current_app
from dotenv import load_dotenv
import requests
import os
def get_ip():
    return request.headers.get('x-real-ip') or request.headers.get('x-forwarded-for', request.remote_addr)


def get_city_from_ip(ip_address):

    #ip_address = request.headers.get('x-real-ip') or request.headers.get('x-forwarded-for', request.remote_addr)
    
    if os.getenv("VERCEL"):
    # Load environment variables from Vercel secrets
        access_key = os.environ.get('IP_KEY')
    else:
    # Load environment variables from the .env file
        load_dotenv()
        access_key= os.environ.get("IP_FINDER")

    #url = f"http://api.ipstack.com/2a0c:5bc0:40:11c4:631c:ac68:22c6:440?access_key={access_key}"
    url = f"http://api.ipstack.com/{ip_address}?access_key={access_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if 'city' in data:
            city = data['city']
            return city
        else:
            return "City information not found for this IP address"

    except requests.RequestException as e:
        return f"Error: {e}"


def get_country_from_ip(ip_address):
    # ip_address = request.headers.get('x-real-ip') or request.headers.get('x-forwarded-for', request.remote_addr)

    if os.getenv("VERCEL"):
        # Load environment variables from Vercel secrets
        access_key = os.environ.get('IP_KEY')
    else:
        # Load environment variables from the .env file
        load_dotenv()
        access_key = os.environ.get("IP_FINDER")

    # url = f"http://api.ipstack.com/2a0c:5bc0:40:11c4:631c:ac68:22c6:440?access_key={access_key}"
    url = f"http://api.ipstack.com/{ip_address}?access_key={access_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if 'country' in data:
            country = data['city']
            return country
        else:
            return "City information not found for this IP address"

    except requests.RequestException as e:
        return f"Error: {e}"