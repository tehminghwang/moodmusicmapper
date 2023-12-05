from dotenv import load_dotenv
import requests
import os


def test_get_location():
    if os.getenv("VERCEL"):
        # Load environment variables from Vercel secrets
        access_key = os.environ.get("IP_KEY")
    elif os.getenv("GIT_IP"):
        access_key = os.environ.get("GIT_IP")
    else:
        # Load environment variables from the .env file
        load_dotenv()
        access_key = os.environ.get("IP_FINDER")

    ip_address = "178.128.45.18"
    url = f"http://api.ipstack.com/{ip_address}?access_key={access_key}"

    response = requests.get(url)
    data = response.json()

    assert data["city"] == "South Croydon"
    assert data["country_name"] == "United Kingdom"
    assert data["country_code"] == "GB"
