import flask
from flask import request, jsonify

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
load_dotenv()

import os

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
	return "<h1>Spotify - Procurar artista</h1><p>Endpoint: /api/v1/artists/search/[query]</p><p>Descrição: Retorna os artistas (nome, image, url do spotify e uri - identificador da api do spotify) que correspondem a query</p>"


@app.route('/api/v1/artists/search/<name>', methods=['GET'])
def get_artist(name):
	results = []

	spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

	received = spotify.search(q='artist:' + name, type='artist')
	items = received['artists']['items']

	print("items found: ", len(items))

	for artist in items:
		new_name = artist['name']
		new_image = artist['images'][0]['url'] if len(artist['images']) > 0 else ''
		new_spotify_url = artist['external_urls']['spotify']
		new_uri = artist['uri']

		new = { 'name': new_name, 'image': new_image, 'spotify_url': new_spotify_url, 'uri': new_uri }

		results.append(new)

	return jsonify(results)



app.run()


