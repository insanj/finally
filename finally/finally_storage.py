#!/usr/bin/python
import os
import glob
from finally_importer import *
from finally_parser import *
from finally_storage_json import *
from external import *

class FinallyStorage:
	songs = []
	providers = []

	def __init__(self, providers=[FinallyStorageJSONProvider()], path="exports"):
		self.path = path
		self.providers = providers
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
		path = self.currentPath()
		for provider in self.providers:
			provider.save(self.songs, path)

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