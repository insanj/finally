#!/usr/bin/python
import cgi
import json
from finally_parser import *
from finally_storage_providers import *

print 'Content-Type: application/json\n\n'
importer = FinallyImporter()
files = importer.findImportableFiles()
parser = FinallySongParser()
songs = []

for file in files:
	songsInFile = parser.parseFileIntoSongs(file)
	for song in songsInFile:
		songs.append(song)
		
jsonSongs = FinallyStorageJSONProvider.convertToJSONArray(songs)
print json.dumps(jsonSongs)