#!/usr/bin/python
from flask import Flask, jsonify, render_template, request
from finally_parser import *
from finally_storage import *
from finally_storage_providers import *
from finally_importer_spotify import *
from finally_main import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route("/run")
def run():
	songs = Finally().main()
	jsonSongs = FinallyStorageJSONProvider.convertToJSONArray(songs)
	return jsonify(jsonSongs)

@app.route("/load")
def load():
	jsonData = open("exports/finally.json").read()
	return jsonData

@app.route("/spotify")
def spotify():
	oauthCode = request.args.get('code', default = '*', type = str)
	print("\nspotify! args = " + str(request.args) + "\n\n code = " + str(oauthCode))
	FinallyStorage.arbitrarySave("oauth", "oauth/spotify.txt", oauthCode)
	return "Saved " + oauthCode
