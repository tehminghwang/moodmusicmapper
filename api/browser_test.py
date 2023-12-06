import requests
from bs4 import BeautifulSoup

# Fetch the website's content
url = "https://moodmusicmapper.vercel.app"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, "html.parser")

def test_carousel_functionality():
    carousel = soup.find('div', class_='carousel-view')
    assert carousel is not None, "Carousel element not found"
    # Check for navigation buttons
    prev_btn = carousel.find('button', id='prev-btn')
    next_btn = carousel.find('button', id='next-btn')
    assert prev_btn is not None, "Previous button not found"
    assert next_btn is not None, "Next button not found"

def test_mood_submission_form():
    form = soup.find('form', action='/submit')
    assert form is not None, "Form not found"
    mood_field = form.find('input', id='moodfield')
    assert mood_field is not None, "Mood input field not found"

def test_navigation_bar_links():
    nav = soup.find('nav', id='nav')
    assert nav is not None, "Navigation bar not found"
    links = nav.find_all('a')
    assert len(links) > 0, "No links found in navigation bar"

def test_banner_content():
    banner = soup.find('section', id='banner')
    assert banner is not None, "Banner section not found"
    banner_content = banner.get_text(strip=True)
    assert banner_content, "Banner content is empty"

def test_responsive_design_elements():
    meta_tag = soup.find('meta', attrs={"name": "viewport"})
    assert meta_tag is not None, "Viewport meta tag for responsive design not found"

# Run tests
test_carousel_functionality()
test_mood_submission_form()
test_navigation_bar_links()
test_banner_content()
test_responsive_design_elements()

