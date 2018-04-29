#!/usr/bin/python
from flask import Flask, jsonify, request, render_template, send_from_directory
from finally_parser import *
from finally_storage_providers import *

app = Flask(__name__)

@app.route('/')
def index():
	message = "Hello, world"
	return render_template('index.html', message=message)

@app.route("/run")
def run():
	importer = FinallyImporter()
	files = importer.findImportableFiles()
	parser = FinallySongParser()
	songs = []

	for file in files:
		songsInFile = parser.parseFileIntoSongs(file)
		for song in songsInFile:
			songs.append(song)
		
	jsonSongs = FinallyStorageJSONProvider.convertToJSONArray(songs)
	return jsonify(jsonSongs)