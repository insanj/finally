#!/usr/bin/python
import os
import json
from finally_song import *
from finally_storage import *

class FinallyStorageProvider:
	def save(self, songs, path):
		raise ValueException("FinallyStorageProvider no-op")

class FinallyStorageJSONProvider(FinallyStorageProvider):
	def save(self, songs, path):
		songJSONDict = []
		for song in songs:
			songJSONDict.append(song.convertToJSON())

		filename = os.path.join(path, "storage.finally")
		jsonString = json.dumps(songJSONDict)
		with open(filename, 'w') as storingFile:
			storingFile.write(jsonString)