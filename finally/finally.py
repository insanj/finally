#!/usr/bin/python
from finally_parser import *
from finally_storage import *

class Finally:
	def main(self):
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

		print "***** Finished! *****"

if __name__ == "__main__":
	Finally().main()