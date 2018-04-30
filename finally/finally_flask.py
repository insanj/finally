#!/usr/bin/python
from flask import Flask, jsonify, render_template
from finally_parser import *
from finally_storage import *
from finally_storage_providers import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

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
		
	storage = FinallyStorage()
	for song in songs:
		storage.storeSong(song)

	storage.save()
	
	jsonSongs = FinallyStorageJSONProvider.convertToJSONArray(songs)
	return jsonify(jsonSongs)

@app.route("/load")
def load():
	jsonData = open("exports/finally.json").read()
	return jsonData
