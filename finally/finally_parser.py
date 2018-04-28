#!/usr/bin/python
import datetime
from finally_song import *

class FinallySongParser:
	def parseFileIntoSongs(file):


	def parseSong(fileData):
		# detect data type

	def parseSpotifySong(spotifyData):

		originIdentifier = FinallySongOrigin.spotifyIdentifier()
		origin = FinallySongOrigin(originIdentifier, datetime.datetime.utcnow()) 
		parsedSong = FinallySong(originIdentifier)

		parsedSong.name =

	def parseiTunesSong(iTunesData):
