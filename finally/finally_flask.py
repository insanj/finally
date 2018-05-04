#!/usr/bin/python
from flask import Flask, jsonify, render_template, request
import os
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
	finallyLoadPath = "exports/finally.json"
	if not os.path.exists(finallyLoadPath):
		return jsonify({"error" : {"status" : "404", "message" : "Finally JSON library file not found, " + finallyLoadPath}});
	else:
		jsonData = open(finallyLoadPath).read()
		return jsonData

@app.route("/spotify")
def spotify():
	oauthCode = request.args.get('code', default = '*', type = str)
	print("\nspotify! args = " + str(request.args) + "\n\n code = " + str(oauthCode))
	FinallyStorage.arbitrarySave("oauth", "oauth/spotify.txt", oauthCode)
	closeItselfDocument = "<html><body><script>window.close();</script></body></html>"
	return closeItselfDocument