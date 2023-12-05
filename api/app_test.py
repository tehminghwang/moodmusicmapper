import json
from app import hello_world
from flask import request, render_template
from unittest.mock import patch, MagicMock

# Test when there is no cookie
def test_hello_world_no_cookie():
    with patch.object(request, 'cookies', new_callable=MagicMock(return_value={})):
        with patch('your_module.render_template') as mock_render:
            hello_world()
            mock_render.assert_called_once_with("index.html", mood=None)

# Test with valid cookie
def test_hello_world_valid_cookie():
    valid_playlist = [('playlist', '[{"name": "Christmas Lights", "artist": "Coldplay", "uri": "4fzyvSu73BhGvi96p2zwjL", "artist_uri": "4gzpq5DPGxSnKTe4SA8HAU"}, {"name": "All I Want for Christmas Is You", "artist": "Mariah Carey", "uri": "0bYg9bo50gSsH3LtXe2SQn", "artist_uri": "4iHNK0tOyZPYnBU7nGAgpQ"}]')]
    with patch.object(request, 'cookies', new_callable=MagicMock(return_value={'playlist': json.dumps(valid_playlist)})):
        with patch('your_module.render_template') as mock_render:
            hello_world()
            mock_render.assert_called_once_with("index.html", mood=valid_playlist)


# Test with invalid cookie
def test_hello_world_invalid_cookie():
    with patch.object(request, 'cookies', new_callable=MagicMock(return_value={'playlist': 'invalid json'})):
        with patch('your_module.render_template') as mock_render:
            hello_world()
            mock_render.assert_called_once_with("index.html", mood=None)
