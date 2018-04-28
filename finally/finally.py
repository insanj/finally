#!/usr/bin/python

class Finally:
	def main():
		importer = FinallyImporter()
		files = importer.findImportableFiles()

		parser = FinallySongParser()
		storage = FinallyStorage()

		for file in files:
			songsInFile = parser.parseFileIntoSongs(file)
			for song in songsInFile:
				storage.storeSong(song)

		print "***** Finished! *****"