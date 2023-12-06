import json
import pytest
from flask import Flask, request, render_template
from app import app
import database, ipfinder
from unittest.mock import patch, MagicMock


# Test when there is no cookie
def test_hello_world_no_cookie():
    with app.test_client() as client:
        with patch("app.render_template") as mock_render:
            total = database.total_recommendations()
            response = client.get("/")
            mock_render.assert_called_once_with("index.html", mood=None, total=total)


# Test with valid cookie
def test_hello_world_valid_cookie():
    valid_playlist = '[{"name": "Christmas Lights", "artist": "Coldplay"}]'
    with app.test_client() as client:
        with patch("app.render_template") as mock_render:
            client.set_cookie("playlist", valid_playlist)
            total = database.total_recommendations()
            response = client.get("/")
            mock_render.assert_called_once_with(
                "index.html", mood=json.loads(valid_playlist), total=total
            )


# Test with invalid cookie
def test_hello_world_invalid_cookie():
    invalid_playlist = "[{......////////.....}]"
    with app.test_client() as client:
        with patch("app.render_template") as mock_render:
            client.set_cookie("playlist", invalid_playlist)
            total = database.total_recommendations()
            response = client.get("/")
            mock_render.assert_called_once_with("index.html", mood=None, total=total)
