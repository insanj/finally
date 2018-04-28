#!/usr/bin/python
import json
import glob
import os
from finally_file import FinallyFile

class FinallyImporter:
	def __init__(self, path="imports"):
		self.path = os.path.join(os.getcwd(), path)

	def getContentsOfFilePath(self, filePath):
		relativeFilePath = filePath
		with open(filePath) as fileContents:
			return fileContents.read()

	def findImportableFilePaths(self):
		globPath = os.path.join(self.path, "*")
		return glob.glob(globPath)
	
	def findImportableFiles(self):
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