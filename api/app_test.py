import json
import pytest
from flask import Flask, request, render_template
from app import app
from unittest.mock import patch, MagicMock


# Test when there is no cookie
def test_hello_world_no_cookie():
    with app.test_client() as client:
        with patch('app.render_template') as mock_render:
            response = client.get('/')
            mock_render.assert_called_once_with("index.html", mood=None)


# Test with valid cookie
def test_hello_world_valid_cookie():
    valid_playlist = '[{"name": "Christmas Lights", "artist": "Coldplay"}]'
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['playlist'] = valid_playlist  # Set the cookie in the session
        with patch('app.render_template') as mock_render:
            response = client.get('/')
            mock_render.assert_called_once_with("index.html", mood=json.loads(valid_playlist))


# Test with invalid cookie
#def test_hello_world_invalid_cookie():
#    with app.test_request_context('/'):
#        with patch('flask.request.cookies', new=MagicMock(return_value={'playlist': 'invalid json'})):
#            with patch('flask.render_template') as mock_render:
#                app.hello_world()
#                mock_render.assert_called_once_with("index.html", mood=None)
