#!/usr/bin/python
import datetime
import xmltodict
import xml.etree.ElementTree
from finally_importer import *
from finally_song import *
from finally_file import *
from finally_storage import *
from external import *

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

	def parseSpotifyJSONIntoSong(self, songJSON, jsonPath):
		originIdentifier = FinallySongOrigin.spotifyIdentifier()
		origin = FinallySongOrigin(originIdentifier, datetime.datetime.utcnow(), jsonPath) 

		jsonSongValues = songJSON["track"]
		parsedSongValues = {}
		parsedSongValues["name"] = jsonSongValues["name"].encode('utf-8')
		parsedSongValues["identifier"] = jsonSongValues["id"]
		parsedSongValues["album"] = jsonSongValues["album"]
		parsedSongValues["artists"] = jsonSongValues["artists"]
		parsedSong = FinallySong(origin, parsedSongValues)

		return parsedSong

	def parseSpotifyFileIntoSongs(self, file):
		jsonDump = json.loads(file.contents)
		jsonTracks = jsonDump["items"]
		parsedSongs = []
		for track in jsonTracks:
			parsedSongs.append(self.parseSpotifyJSONIntoSong(track, file.path))

		return parsedSongs

	def checkIfiTunesFile(self, file):
		return file.path.endswith('.xml')

	def parseiTunesXMLIntoSong(self, songXML, xmlPath):
		originIdentifier = FinallySongOrigin.iTunesIdentifier()
		origin = FinallySongOrigin(originIdentifier, datetime.datetime.utcnow(), xmlPath) 
		
		parsedSongValues = {}
		xmlSongStringValues = songXML["string"]
		parsedSongValues["name"] = xmlSongStringValues[0].encode('utf-8') # indexes given in keys array
		
		xmlSongIntegerValues = songXML["integer"]
		parsedSongValues["identifier"] = str(xmlSongIntegerValues[0])

		parsedSongValues["artists"] = [str(xmlSongStringValues[1]), str(xmlSongStringValues[2])]

		parsedSong = FinallySong(origin, parsedSongValues)
		return parsedSong

	def debugiTunesXML(self, xmlFileDict):
		tmpstr = ">"
		tmpstr += str(xmlFileDict)
		#tmpstr += ">plist"
		#tmpstr += str(xmlFileDict["plist"])
		#tmpstr += ">plist>dict"
		#tmpstr += str(xmlFileDict["plist"]["dict"])
		#tmpstr += ">plist>dict>dict"
		#tmpstr += str(xmlFileDict["plist"]["dict"]["dict"])
		#tmpstr += ">plist>dict>dict>dict"
		#tmpstr += str(xmlFileDict["plist"]["dict"]["dict"]["dict"])
		tmppath = os.path.join(os.getcwd(), "logs")
		tmpfilepath = os.path.join(tmppath, "finallyituneslog.json")
		FinallyStorage.arbitrarySave(tmppath, tmpfilepath, tmpstr)
		print("saved")
		return False

	def parseiTunesFileIntoSongs(self, file):
		#xmlFileDict = xmltodict.parse(file.contents)
		xmlFileTree = xml.etree.ElementTree.fromstring(file.contents)
		xmlFileDict = make_dict_from_tree(xmlFileTree)

		if self.debugiTunesXML(xmlFileDict) == False:
			return None

		xmlTrackDicts = xmlFileDict["plist"]["dict"]["dict"]
		print(xmlTrackDicts)
		parsedSongs = []
		for xmlTrack in xmlTrackDicts:
			parsedSongs.append(self.parseiTunesXMLIntoSong(xmlTrack, file.path))

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
			print("Parsed song = " + song.metadata.name)

	#file = defaultFiles[1]
	#print("Parsing file = " + file.path)
	#parsedSongs = defaultParser.parseFileIntoSongs(file)
	#parsedFile = file
	#parsedFile.parsedSongs = parsedSongs
	#parsedFiles.append(parsedFile)

	#for file in parsedFiles:
	#	print("Parsed file = " + parsedFile.path)
	#	for song in file.parsedSongs:
	#		print("Parsed song = " + song.metadata.name)

	print("Finished!")
