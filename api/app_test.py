import json
import pytest
from flask import Flask, request, render_template
from app import app
import database, ipfinder
from unittest.mock import patch, MagicMock


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
            client.set_cookie('city', 'test_city')
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


