#!/usr/bin/python
import datetime
from finally_song import *
import xml.etree.ElementTree

class FinallySongParser:
	def parseFileIntoSongs(self, file): # main entry point
		if self.checkIfSpotifyFile(file):
			return self.parseSpotifyFileIntoSongs(file)

		elif self.checkIfiTunesFile(file):
			return self.parseiTunesFileIntoSongs(file)

		else:
			return None

	def checkIfSpotifyFile(self, file):
		return file.path.endswith('.json'):

	def parseSpotifyJSONIntoSong(self, songJSON):
		originIdentifier = FinallySongOrigin.spotifyIdentifier()
		origin = FinallySongOrigin(originIdentifier, datetime.datetime.utcnow()) 
		parsedSong = FinallySong(originIdentifier)
		return parsedSong

	def parseSpotifyFileIntoSongs(self, file):
		jsonDump = json.dumps(file)
		jsonSongs = []
		for key in jsonDump:
			if key == "songs":
				for jsonDumpSong in jsonDump[key]:
					jsonSongs.append(jsonDumpSong)

		parsedSongs = []
		for jsonSong in jsonSongs:
			parsedSongs.append(self.parseSpotifyJSONIntoSong(jsonSong))

	def checkIfiTunesFile(self, file):
		return file.path.endswith('.xml')

	def parseiTunesXMLIntoSong(self, songXML):
		originIdentifier = FinallySongOrigin.iTunesIdentifier()
		origin = FinallySongOrigin(originIdentifier, datetime.datetime.utcnow()) 
		parsedSong = FinallySong(originIdentifier)
		return parsedSong

	def parseiTunesFileIntoSongs(self, file):
		xmlFileRoot = xml.etree.ElementTree.fromstring(file.contents)
		xmlTracksDict = xmlFileRoot.find("Tracks")
		parsedSongs = []
		for trackKey in xmlTracksDict:
			trackContents = xmlTracksDict[trackKey]
			parsedSongs.append(self.parseiTunesXMLIntoSong(trackContents))

		return parsedSongs