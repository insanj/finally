#!/usr/bin/python
from flask import Flask, jsonify
from finally_parser import *
from finally_storage_providers import *

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
	with open("../index.html") as fileContents:
		return fileContents.read()

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
