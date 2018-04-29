#!/usr/bin/python
import json
import uuid
import datetime

class FinallySong:
	origin = None
	metadata = None

	def __init__(self, origin, metadata={}):
		self.origin = origin
		self.metadata = metadata

	def serializedMetadata(self):
		jsonableMetadata = {}
		for key in self.metadata.keys():
			value = self.metadata[key]
			if isinstance(value, datetime.datetime):
				jsonableMetadata[key] = str(value)
			else:
				jsonableMetadata[key] = value

		return json.dumps(jsonableMetadata)

	def serializedOrigin(self):
		return self.origin.serializable()

	def convertToJSON(self):
		metadataWithOrigin = {"origin" : self.serializedOrigin(), "metadata" : self.serializedMetadata()}
		return json.dumps(metadataWithOrigin, default=lambda o: o.__dict__)

class FinallySongOrigin:
	identifier = None
	timestamp = None
	path = None
	def __init__(self, identifier, timestamp, path):
		if identifier not in FinallySongOrigin.validIdentifiers():
			raise ValueError("[FinallySongOrigin] invalid identifier") 

		self.identifier = identifier
		self.timestamp = timestamp
		self.path = path

	def serializable(self):
		return FinallySongOrigin(self.identifier, str(self.timestamp), self.path)

	@classmethod
	def spotifyIdentifier(self):
		return "spotify"

	@classmethod
	def iTunesIdentifier(self):
		return "itunes"

	@classmethod
	def validIdentifiers(self):
		return [FinallySongOrigin.spotifyIdentifier(), FinallySongOrigin.iTunesIdentifier()]
