import json
import pytest
from flask import Flask, request, render_template
from app import app
import database, ipfinder
from unittest.mock import patch, MagicMock


# Test when there is no cookie
def test_hello_world_no_cookie():
    with app.test_client() as client:
        with patch('app.render_template') as mock_render:
            total = database.total_recommendations()
            response = client.get('/')
            mock_render.assert_called_once_with("index.html", mood=None, total=total)


# Test with valid cookie
def test_hello_world_valid_cookie():
    valid_playlist = '[{"name": "Christmas Lights", "artist": "Coldplay"}]'
    with app.test_client() as client:
        with patch('app.render_template') as mock_render:
            client.set_cookie('playlist', valid_playlist)
            total = database.total_recommendations()
            response = client.get('/')
            mock_render.assert_called_once_with("index.html", mood=json.loads(valid_playlist), total=total)


# Test with invalid cookie
def test_hello_world_invalid_cookie():
    invalid_playlist = '[{......////////.....}]'
    with app.test_client() as client:
        with patch('app.render_template') as mock_render:
            client.set_cookie('playlist', invalid_playlist)
            total = database.total_recommendations()
            response = client.get('/')
            mock_render.assert_called_once_with("index.html", mood=None, total=total)


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


# Test response page with valid input mood
def test_response_page_valid_input():
    test_mood = 'happy'

    with app.test_client() as client:
        with patch('app.send_request') as mock_send_request, \
                patch('app.extract_values') as mock_extract_values, \
                patch('spotify_mod.spotify_main') as mock_spotify_main, \
                patch('database.display_phrase') as mock_display_phrase, \
                patch('database.song_of_day') as mock_song, \
                patch('app.create_map') as mock_create_map, \
                patch('spotify_mod.get_artist_top_song') as mock_artist, \
                patch('app.render_template') as mock_render:
            # Mock responses
            client.set_cookie('localhost', 'city', 'test_city')
            mock_send_request.return_value = 'mock_reply'
            mock_extract_values.return_value = (0.5, 0.5, 0.5, 'happy', 'pop', 'Song1', 'Singer1', 'Song2', 'Singer2', 'Song3', 'Singer3')
            mock_spotify_main.return_value = ['playlist_item1', 'playlist_item2']
            mock_display_phrase.return_value = 'mood_phrase'
            mock_create_map.return_value = 'mock_map'
            mock_render.return_value = 'mock_html'
            mock_artist.return_value = 'mock_artist'
            mock_song.return_value = 'mock_song'

            response = client.get(f'/response/{test_mood}')
            assert response.status_code == 200

            # Adjust expected_render_args as per actual arguments passed in render_template
            expected_render_args = {
                'input_mood': test_mood,
                'mood_phrase': 'mood_phrase',
                'mood': 'happy',
                'playlist': ['playlist_item1', 'playlist_item2'],
                'response': 'Valency: 0.5, Danceability: 0.5, Energy: 0.5, Mood: happy',
                'reply': 'mock_reply',
                'city': 'test_city',
                'map_html': 'mock_map',
                'song_of_day': 'mock_song',
                'singer_of_day_top_song': 'mock_artist'
            }
            mock_render.assert_called_once_with("mood.html", **expected_render_args)



# Test response page with invalid mood
def test_response_page_invalid_input():
    test_mood = ''
    with app.test_client() as client:
        response = client.get(f'/response/{test_mood}')
        assert response.status_code == 404


# test response page with exception handling
def test_response_page_exception():
    test_mood = 'happy'
    with app.test_client() as client:
        with patch('app.send_request') as mock_send_request:
            with patch('app.render_template') as mock_render:
                mock_send_request.side_effect = Exception("Test exception")
                response = client.get(f'/response/{test_mood}')
                assert response.status_code == 200
                mock_render.assert_called_once_with("error.html")


# Test cookie setting in response page
def test_response_page_cookie_setting():
    test_mood = 'happy'

    with app.test_client() as client:
        with patch('app.send_request') as mock_send_request, \
             patch('app.extract_values') as mock_extract_values:

            mock_send_request.return_value = 'mock_reply'
            mock_extract_values.return_value = (0.5, 0.5, 0.5, 'happy', 'pop', 'Song1', 'Singer1', 'Song2', 'Singer2', 'Song3', 'Singer3')

            response = client.get(f'/response/{test_mood}')
            cookies = response.headers.getlist('Set-Cookie')
            assert any('playlist=' in cookie for cookie in cookies)


