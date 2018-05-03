#!/usr/bin/python
from finally_parser import *
from finally_storage import *
from finally_importer import *
from finally_storage_providers import *
from finally_importer_spotify import *

class Finally:
	def main(self):
		print "[Finally] Starting up! Finding importable files..."
		importer = FinallyImporter()
		files = importer.importFiles()
		parser = FinallySongParser()
		songs = []
		print "[Finally] Parsing "+str(len(files))+" files in imports directory..."
		for file in files:
			songsInFile = parser.parseFileIntoSongs(file)
			for song in songsInFile:
				songs.append(song)

		spotifyImporter = FinallySpotifyImporter()
		spotifyLibrary = spotifyImporter.importLibrary()
		spotifyLibraryFile = FinallyFile("online", spotifyLibrary)
		parsedSpotifyLibrarySongs = parser.parseSpotifyFileIntoSongs(spotifyLibraryFile)

		for song in parsedSpotifyLibrarySongs:
			songs.append(song)

		print "[Finally] Aggregating "+str(len(songs))+" songs together and exporting..."
		storage = FinallyStorage()
		for song in songs:
			storage.storeSong(song)

		storage.save()
		print "[Finally] Finished exporting into both JSON and sqlite!"

		return songs

if __name__ == "__main__":
	Finally().main()