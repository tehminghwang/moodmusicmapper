import requests
from bs4 import BeautifulSoup

url = 'https://moodmusicmapper.vercel.app'

reqs = requests.get(url)

soup = BeautifulSoup(reqs.text, 'html.parser')


def test_knows_about_mmm_title():
    for title in soup.find_all('title'):
        assert title.getText() == 'Magic Music Mapper'