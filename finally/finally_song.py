#!/usr/bin/python
import json
import uuid
import datetime

class FinallySong:
	origin = None
	metadata = None
	finallyMetadata = None

	def __init__(self, origin, metadata={}):
		self.origin = origin
		self.metadata = metadata
		self.finallyMetadata = FinallySongMetadata(origin, metadata)

	def serializedOrigin(self):
		return self.origin.serializable()

	def serializedMetadata(self):
		jsonableMetadata = {}
		for key in self.metadata.keys():
			value = self.metadata[key]
			if isinstance(value, datetime.datetime):
				jsonableMetadata[key] = str(value)
			else:
				jsonableMetadata[key] = value

		return json.dumps(jsonableMetadata)

	def serializedFinallyMetadata(self):
		return self.finallyMetadata.serializable()

	def convertToJSON(self):
		metadataWithOrigin = {"origin" : self.serializedOrigin(), "metadata" : self.serializedMetadata(), "finallyMetadata" : self.serializedFinallyMetadata()}
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

class FinallySongMetadata:
	origin = None
	name = None
	artist = None
	album = None
	duration = None

	def __init__(self, origin, metadata):
		self.parseMetadata(origin, metadata)

	def parseMetadata(self, origin, metadata):
		if origin.identifier == "spotify":
			self.parseSpotifyMetadata(metadata)
		else:
			self.parseiTunesMetadata(metadata)

	def parseSpotifyMetadata(self, metadata):
		keys = metadata.keys()
		if "name" in keys:
			self.name = metadata["name"]
		if "artists" in keys:
			self.artist = metadata["artists"][0]["name"]
		if "album" in keys:
			self.album = metadata["album"]["name"]
		if "duration_ms" in keys:
			self.duration = metadata["duration_ms"]

	def parseiTunesMetadata(self, metadata):
		keys = metadata.keys()
		if "Name" in keys:
			self.name = metadata["Name"]
		if "Artist" in keys:
			self.artist = metadata["Artist"]
		if "Album" in keys:
			self.album = metadata["Album"]
		if "Total Time" in keys:
			self.duration = metadata["Total Time"]

	def serializable(self):
		return self