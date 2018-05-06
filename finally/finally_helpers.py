#!/usr/bin/python

class FinallyConfig:
	debugPrinting = None
	importFromOnline = None
	importFromOffline = None
	exportFinallyLibrary = None

	def __init__(self, importFromOnline=True, importFromOffline=True, debugPrinting=True, exportFinallyLibrary=True):
		self.importFromOnline = importFromOnline
		self.importFromOffline = importFromOffline
		self.debugPrinting = debugPrinting
		self.exportFinallyLibrary = exportFinallyLibrary

class FinallyLogger:
	config = None

	def __init__(self, config=FinallyConfig()):
		self.config = config

	def _printWithLevel(self, preappend, string):
		if self.config.debugPrinting is True:
			print preappend + string

	def log(self, logString):
		self._printWithLevel("L:", logString)

	def error(self, errString):
		self._printWithLevel("E:", errString)