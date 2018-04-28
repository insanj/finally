#!/usr/bin/python
import os
import glob
from finally_importer import *
from finally_parser import *
from seanh_formatFilename import *

class FinallyStorage:
	songs = []

	def __init__(self, path="exports"):
		self.path = path
		self.createPathIfNeeded()

	def createPathIfNeeded(self):
		cp = self.currentPath()
		if not os.path.exists(cp):
			os.makedirs(cp)

	def currentPath(self):
		return os.path.join(os.getcwd(), self.path)

	def storeSong(self, song):
		self.songs.append(song)

	def save(self):
		songJSONDict = []
		for song in self.songs:
			songJSONDict.append(song.convertToJSON())

		filename = os.path.join(self.currentPath(), "storage.finally")
		jsonString = json.dumps(songJSONDict)
		with open(filename, 'w') as storingFile:
			storingFile.write(jsonString)

if __name__ == "__main__":
	print("***** Default FinallyStorage results: *****")
	defaultImporter = FinallyImporter()
	defaultFiles = defaultImporter.findImportableFiles()
	file = defaultFiles[1]
	print("Storing song from file = " + file.path)

	defaultParser = FinallySongParser()
	parsedSongs = defaultParser.parseFileIntoSongs(file)
	song = parsedSongs[0]
	print("Storing song = " + song.name)

	defaultStorage = FinallyStorage()
	defaultStorage.storeSong(song)

	print("Finished!")