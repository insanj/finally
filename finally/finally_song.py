#!/usr/bin/python
import json
import uuid

class FinallySongOrigin:
	identifier = None
	timestamp = None
	def __init__(self, identifier, timestamp):
		if identifier not in FinallySongOrigin.validIdentifiers():
			raise ValueError("[FinallySongOrigin] invalid identifier") 

		self.identifier = identifier
		self.timestamp = timestamp

	@classmethod
	def spotifyIdentifier(self):
		return "spotify"

	@classmethod
	def iTunesIdentifier(self):
		return "itunes"

	@classmethod
	def validIdentifiers(self):
		return [FinallySongOrigin.spotifyIdentifier(), FinallySongOrigin.iTunesIdentifier()]

class FinallySong:
	origin = None
	name = None
	identifier = uuid.uuid1()
	
	def __init__(self, origin):
		self.origin = origin

	def convertToJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__)
