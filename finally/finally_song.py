#!/usr/bin/python

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
	def __init__(self, origin):
		self.origin = origin