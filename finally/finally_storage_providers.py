#!/usr/bin/python
import os
import json
import sqlite3
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
	def save(self, songs):
		songJSONDict = []
		for song in songs:
			songJSONDict.append(song.convertToJSON())

		filename = os.path.join(self.path, "finally.json")
		jsonString = json.dumps(songJSONDict)
		with open(filename, 'w') as storingFile:
			storingFile.write(jsonString)

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
		songTableQuery = "CREATE TABLE IF NOT EXISTS " + self.tableName + "(id INTEGER PRIMARY KEY AUTOINCREMENT, identifier TEXT, name TEXT)"
		self.cursor.execute(songTableQuery)
		self.database.commit()

	def executeDatabaseQuery(self, query):
		self.cursor.execute(query)
		self.database.commit()

	def closeDatabase(self):
		self.database.close()

	def getSaveQueryForSong(self, song):
		return "INSERT INTO " + self.tableName + " (identifier, name) VALUES(?, ?)"
		# return "INSERT INTO " + self.tableName + "(identifier, name) VALUES('" + song.identifier + "', '" + encodedName + "')"

	def save(self, songs):
		self.openDatabase()

		for song in songs:
			query = self.getSaveQueryForSong(song)
			encodedSongName = format_filename(song.name)
			print("saving name = " + encodedSongName)
			self.cursor.execute(query, (song.identifier, encodedSongName))
			self.database.commit()

		self.closeDatabase()