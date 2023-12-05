import json
import pytest
from flask import Flask, request, render_template
from app import app
import database, ipfinder
from unittest.mock import patch, MagicMock


# Test Submit with No IP Cookie and Valid Form Data
def test_submit_no_ip_cookie():
    with app.test_client() as client:
        with patch('ipfinder.get_ip') as mock_get_ip, \
                patch('ipfinder.get_location_from_ip') as mock_get_location:
            mock_get_ip.return_value = '123.456.789.0'
            mock_get_location.return_value = {'city': 'TestCity', 'country': 'TestCountry', 'country_code': 'TC'}

            form_data = {'mood': 'happy'}
            response = client.post('/submit', data=form_data)

            # Check response and cookies set
            assert response.status_code == 302  # Redirect status
            cookies = response.headers.getlist('Set-Cookie')
            assert any('ipaddress=123.456.789.0' in cookie for cookie in cookies)
            assert any('city=TestCity' in cookie for cookie in cookies)
            assert any('country=TestCountry' in cookie for cookie in cookies)
            assert any('country_code=TC' in cookie for cookie in cookies)


# Test Submit with Existing IP Cookie
def test_submit_with_ip_cookie():
    with app.test_client() as client:
        client.set_cookie('ipaddress', '123.456.789.0')
        form_data = {'mood': 'sad'}
        response = client.post('/submit', data=form_data)

        # Check for redirect and no additional IP address cookie set
        assert response.status_code == 302  # Redirect status
        assert 'ipaddress' in request.cookies
        assert request.cookies['ipaddress'] == '123.456.789.0'


# Test Submit with Empty Form Data
def test_submit_invalid_form_data():
    with app.test_client() as client:
        form_data = {}  # Empty form data
        response = client.post('/submit', data=form_data)

        # Check response
        assert response.status_code == 302 # Redirect status


# Test loading page with a specific mood
def test_loading_page():
    test_mood = 'happy'
    test_uri = 'test_song_uri'
    with app.test_client() as client:
        with patch('database.song_of_day') as mock_song_of_day:
            # Mock the return value of the song_of_day function
            mock_song_of_day.return_value = test_uri

            # Make a GET request to the loading page route
            response = client.get(f'/loading/{test_mood}')

            # Test status and response
            assert response.status_code == 200
            assert test_mood in response.get_data(as_text=True)
            assert test_uri in response.get_data(as_text=True)

