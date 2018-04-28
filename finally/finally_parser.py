#!/usr/bin/python
import datetime
import xml.etree.ElementTree
from finally_importer import *
from finally_song import *
from finally_file import *
from eric_scrivner_xml import *

class FinallySongParser:
	def parseFileIntoSongs(self, file): # main entry point
		if self.checkIfSpotifyFile(file):
			return self.parseSpotifyFileIntoSongs(file)

		elif self.checkIfiTunesFile(file):
			return self.parseiTunesFileIntoSongs(file)

		else:
			return None

	def checkIfSpotifyFile(self, file):
		return file.path.endswith('.json')

	def parseSpotifyJSONIntoSong(self, songJSON):
		originIdentifier = FinallySongOrigin.spotifyIdentifier()
		origin = FinallySongOrigin(originIdentifier, datetime.datetime.utcnow()) 
		
		parsedSong = FinallySong(originIdentifier)
		parsedSong.name = songJSON["track"]["name"].encode('utf-8')

		return parsedSong

	def parseSpotifyFileIntoSongs(self, file):
		jsonDump = json.loads(file.contents)
		jsonTracks = jsonDump["items"]
		parsedSongs = []
		for track in jsonTracks:
			parsedSongs.append(self.parseSpotifyJSONIntoSong(track))

		return parsedSongs

	def checkIfiTunesFile(self, file):
		return file.path.endswith('.xml')

	def parseiTunesXMLIntoSong(self, songXML):
		originIdentifier = FinallySongOrigin.iTunesIdentifier()
		origin = FinallySongOrigin(originIdentifier, datetime.datetime.utcnow()) 
		
		parsedSong = FinallySong(originIdentifier)
		parsedSong.name = songXML["string"][0].encode('utf-8') # indexes given in keys array

		return parsedSong

	def parseiTunesFileIntoSongs(self, file):
		xmlFileTree = xml.etree.ElementTree.fromstring(file.contents)
		xmlFileDict = make_dict_from_tree(xmlFileTree)
		xmlTracksList = xmlFileDict["plist"]["dict"]["dict"]["dict"] # hopefully
		parsedSongs = []
		for xmlTrack in xmlTracksList:
			parsedSongs.append(self.parseiTunesXMLIntoSong(xmlTrack))

		return parsedSongs

if __name__ == "__main__":
	print("***** Default FinallyParser results: *****")
	defaultImporter = FinallyImporter()
	defaultFiles = defaultImporter.findImportableFiles()
	defaultParser = FinallySongParser()
	parsedFiles = []

	file = defaultFiles[0]
	print("Parsing file = " + file.path)
	parsedSongs = defaultParser.parseFileIntoSongs(file)
	parsedFile = file
	parsedFile.parsedSongs = parsedSongs
	parsedFiles.append(parsedFile)

	for file in parsedFiles:
		print("Parsed file = " + parsedFile.path)
		for song in file.parsedSongs:
			print("Parsed song = " + song.name)

	file = defaultFiles[1]
	print("Parsing file = " + file.path)
	parsedSongs = defaultParser.parseFileIntoSongs(file)
	parsedFile = file
	parsedFile.parsedSongs = parsedSongs
	parsedFiles.append(parsedFile)

	for file in parsedFiles:
		print("Parsed file = " + parsedFile.path)
		for song in file.parsedSongs:
			print("Parsed song = " + song.name)

	print("Finished!")
