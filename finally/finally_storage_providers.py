#!/usr/bin/python
import os
import json
import sqlite3
import sys
from finally_song import *
from finally_storage import *
from external import *

class FinallyStorageProvider:
	path = None

	def __init__(self, path):
		self.path = path

	def save(self, songs):
		raise ValueException("FinallyStorageProvider no-op")

class FinallyStorageJSONProvider(FinallyStorageProvider):
	@classmethod
	def convertToJSONArray(self, songs):
		songJSONArray = []
		for song in songs:
			songJSONArray.append(song.convertToJSON())
		return songJSONArray
		
	def save(self, songs):
		print "[FinallyStorageJSONProvider] saving " + str(len(songs)) + " songs"
		
		songJSONArray = FinallyStorageJSONProvider.convertToJSONArray(songs)
		filename = os.path.join(self.path, "finally.json")
		jsonString = json.dumps(songJSONArray)
		with open(filename, 'w') as storingFile:
			storingFile.write(jsonString)

		print "[FinallyStorageJSONProvider] finished!"

class FinallyStorageMySQLProvider(FinallyStorageProvider):
	tableName = None
	database = None
	cursor = None

	def __init__(self, path):
		self.tableName = "songs"
		self.path = os.path.join(path, "finally.sqlite")

	def openDatabase(self):
		self.database = sqlite3.connect(self.path)
		self.cursor = self.database.cursor()
		songTableQuery = "CREATE TABLE IF NOT EXISTS " + self.tableName + "(id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, file TEXT, timestamp TEXT, metadata TEXT)"
		self.cursor.execute(songTableQuery)
		self.database.commit()

	def executeDatabaseQuery(self, query):
		self.cursor.execute(query)
		self.database.commit()

	def closeDatabase(self):
		self.database.close()

	def getSaveQueryForSong(self, song):
		return "INSERT INTO " + self.tableName + " (type, file, timestamp, metadata) VALUES(?, ?, ?, ?)"

	def save(self, songs):
		print "[FinallyStorageMySQLProvider] saving " + str(len(songs)) + " songs"
		self.openDatabase()

		i = 0
		total = len(songs)
		for song in songs:
			query = self.getSaveQueryForSong(song)
			encodedMetadata = json.dumps(song.metadata)
			self.cursor.execute(query, (song.origin.identifier, song.origin.path, song.origin.timestamp, encodedMetadata))
			self.database.commit()

			i = i + 1
			percent = (float(i)/float(total)) * 100
			print "[FinallyStorageMySQLProvider] {0} {1}/{2} {3}%\r".format(song.origin, i, total, percent),
			sys.stdout.flush()

		self.closeDatabase()
		print "\n[FinallyStorageMySQLProvider] finished!"