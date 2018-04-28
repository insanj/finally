#!/usr/bin/python
from finally_parser import *
from finally_storage import *

class Finally:
	def main(self):
		print "[Finally] Starting up! Finding importable files..."
		importer = FinallyImporter()
		files = importer.findImportableFiles()
		parser = FinallySongParser()
		songs = []
		print "[Finally] Parsing "+str(len(files))+" files in imports directory..."
		for file in files:
			songsInFile = parser.parseFileIntoSongs(file)
			for song in songsInFile:
				songs.append(song)

		print "[Finally] Aggregating "+str(len(songs))+" songs together and exporting..."
		storage = FinallyStorage()
		for song in songs:
			storage.storeSong(song)

		storage.save()
		print "[Finally] Finished exporting into both JSON and sqlite!"

if __name__ == "__main__":
	Finally().main()