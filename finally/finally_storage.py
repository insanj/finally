#!/usr/bin/python
import os
import glob

class FinallyStorage:
	def __init__(self, path="exports"):
		self.path = path

	def storeSong(self, song):
		parsedFilename = self.path + "/" + song.path + ".finally"
		with open(parsedFilename, 'w') as writingFile:
		    writingFile.write(song.contents)
