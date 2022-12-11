from flaskapi import __version__
from flaskapi.app import FlaskAPI
from requests import Session

app = FlaskAPI()

http = Session(
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})


def test_version():
    assert __version__ == '0.1.0'


def test_docs():
    response = http.get('http://localhost:5000/')
    assert response.content_type == 'text/html; charset=utf-8'


def test_api():
    response = http.get('http://localhost:5000/api')
    assert response.content_type == 'application/json'
