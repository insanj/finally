#!/usr/bin/python
import codecs

class FinallyAmazonBruhski:
	def convertBetweenFileEncodings(self, inputPath):
		encoder = codecs.getencoder('utf-8')
		decoder = codecs.getdecoder('utf-8')
		reader = codecs.getreader('latin-1')
		writer = codecs.getwriter('latin-1')
		newFile = codecs.StreamRecoder(inputPath, encoder, decoder, reader, writer)
		return newFile

	def readFileWithUnknownEncoding(self, inputPath):
		with open(inputPath, 'r', encoding="ascii", errors="surrogateescape") as f:
			data = f.read()

		return data

	def readAndConvert(self, inputPath):
		file = self.convertBetweenFileEncodings(inputPath)
		return self.readFileWithUnknownEncoding(file)

if __name__ == "__main__":
	print "[FinallyAmazonBruhski] Hai there! "

	bruhskioni = FinallyAmazonBruhski()
	bruhskioniPath = 'imports/amazon_library.log'
	print bruhskioni.readAndConvert(bruhskioniPath)