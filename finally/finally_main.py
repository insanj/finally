#!/usr/bin/python
from finally_parser import *
from finally_storage import *
from finally_importer import *
from finally_storage_providers import *
from finally_importer_spotify import *

class FinallyConfig:
	debugPrinting = None
	importFromOnline = None
	importFromOffline = None
	exportFinallyLibrary = None

	def __init__(self, importFromOnline=True, importFromOffline=True, debugPrinting=True, exportFinallyLibrary=True):
		self.importFromOnline = importFromOnline
		self.importFromOffline = importFromOffline
		self.debugPrinting = debugPrinting
		self.exportFinallyLibrary = exportFinallyLibrary

class Finally:
	config = None
	parser = None

	def __init__(self, config=FinallyConfig()):
		self.config = config
		self.parser = FinallySongParser()

	def debugPrint(self, string):
		if self.config.debugPrinting is True:
			print "[Finally] " + string

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
		spotifyImporter = FinallySpotifyImporter()
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