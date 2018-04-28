#!/usr/bin/python
import json
import glob
import os

class FinallyFile:
	def __init__(self, path, contents):
		self.path = path
		self.contents = contents

	def size(self):
		return len(self.contents)