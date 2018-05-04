#!/usr/bin/python
import json
import glob
import os
from finally_file import FinallyFile
from finally_importer_spotify import *

class FinallyImporter:
	subimporters = None
	path = None

	def __init__(self, path="imports"):
		self.path = os.path.join(os.getcwd(), path)
		self.subimporters = []

	def checkDirectoryExists(self, dirPath):
		return os.path.exists(dirPath)

	def checkFileExists(self, filePath):
		return os.path.exists(filePath) and os.path.isfile(filePath)

	def getContentsOfFilePath(self, filePath):
		relativeFilePath = filePath
		with open(filePath) as fileContents:
			return fileContents.read()

	def findImportableFilePaths(self):
		globPath = os.path.join(self.path, "*")
		return glob.glob(globPath)
	
	def importFiles(self):
		filePaths = self.findImportableFilePaths()
		importedFiles = []
		for filePath in filePaths:
			contents = self.getContentsOfFilePath(filePath)
			
			importedFile = FinallyFile(filePath, contents)
			importedFiles.append(importedFile)

		return importedFiles

if __name__ == "__main__":
	print("***** Default FinallyImporter results: *****")
	defaultImporter = FinallyImporter()
	results = defaultImporter.findImportableFiles()
	# resultsString = "".join(str(file) for file in results)
	resultsString = ""
	for file in results:
		resultsString += "[FinallyFile] path = " + file.path + ", size = " + str(file.size())
		resultsString += "\n"

	print(resultsString)