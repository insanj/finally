#!/usr/bin/python
from finally_parser import *
from finally_storage import *
from finally_importer import *
from finally_storage_providers import *
from finally_importer_spotify import *
from finally_helpers import *

class Finally:
	config = None
	parser = None
	logger = None

	def __init__(self, config=FinallyConfig()):
		self.config = config
		self.parser = FinallySongParser()
		self.logger = FinallyLogger(config)

	def debugPrint(self, string):
		self.logger.log(string)

	def combineTwoArrays(self, one, two):
		three = one
		for e in two:
			three.append(e)
		return three

	def offlineImportSongs(self):
		importer = FinallyImporter()
		files = importer.importFiles()
		self.debugPrint("OFFLINE Parsing "+str(len(files))+" files in imports directory...")

		songs = []
		for file in files:
			songsInFile = self.parser.parseFileIntoSongs(file)
			songs = self.combineTwoArrays(songs, songsInFile)

		return songs

	def onlineImportSongs(self):
		self.debugPrint("ONLINE importing...")
		spotifyImporter = FinallySpotifyImporter(self.logger)
		spotifyLibrary = spotifyImporter.importLibrary()

		spotifyLibraryFile = FinallyFile("online", spotifyLibrary)
		parsedSpotifyLibrarySongs = self.parser.parseSpotifyFileIntoSongs(spotifyLibraryFile)

		return parsedSpotifyLibrarySongs

	def offlineExportSongs(self, songs):
		self.debugPrint("Aggregating "+str(len(songs))+" songs together and exporting...")
		storage = FinallyStorage()
		for song in songs:
			storage.storeSong(song)

		storage.save()

	def main(self):
		self.debugPrint("Starting up! Finding importable files...")
		songs = []

		if self.config.importFromOffline is True:
			offlineSongs = self.offlineImportSongs()
			songs = self.combineTwoArrays(songs, offlineSongs)
			self.debugPrint("Done importing offline files! Songs grew by " + str(len(offlineSongs)))

		if self.config.importFromOnline is True:
			onlineSongs = self.onlineImportSongs()
			songs = self.combineTwoArrays(songs, onlineSongs)
			self.debugPrint("Done importing online files! Songs grew by " + str(len(onlineSongs)))

		if self.config.exportFinallyLibrary is True:
			self.offlineExportSongs(songs)

		self.debugPrint("Finished importing and exporting " + str(len(offlineSongs)) + " offline songs, " + str(len(onlineSongs)) + " online songs, for a total of " + str(len(songs)) + " songs!")
		return songs

if __name__ == "__main__":
	Finally().main()