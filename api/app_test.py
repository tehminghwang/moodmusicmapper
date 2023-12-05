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
            assert 'ipaddress' in request.cookies
            assert request.cookies['city'] == 'TestCity'
            assert request.cookies['country'] == 'TestCountry'
            assert request.cookies['country_code'] == 'TC'


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


# Test Submit with Invalid Form Data
def test_submit_invalid_form_data():
    with app.test_client() as client:
        form_data = {}  # Empty form data or invalid data
        response = client.post('/submit', data=form_data)

        # Check response
        assert response.status_code == 302  # Assuming redirect behavior even for invalid data



