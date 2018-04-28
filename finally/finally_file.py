#!/usr/bin/python
import json
import glob
import os

class FinallyFile:
	parsedSongs = [] # optional results, included in export

	def __init__(self, path, contents):
		self.path = path
		self.contents = contents

	def size(self):
		return len(self.contents)