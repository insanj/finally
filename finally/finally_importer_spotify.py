#!/usr/bin/python
import httplib, urllib
import webbrowser
import requests
import time
import json
from finally_importer import *

class FinallySubimporter:
	def importLibrary(self):
		raise ValueError("FinallySubimporter no-op must override importLibrary")	

class FinallySpotifyImporter(FinallySubimporter):
	oauthTokenPath = "oauth/spotify.txt"
	authedImporter = None
	unauthedImporter = None

	def importLibrary(self):
		if self.authedImporter is None:
			return self.attemptSpotifyOAuthAndRetryImport()
		else:
			authedLibrary = self.authedImporter.importLibrary()
			if authedLibrary is None: # invalid token
				self.deleteExistingOAuthToken()
				return self.attemptSpotifyOAuthAndRetryImport()

	def deleteExistingOAuthToken(self):
		os.remove(self.oauthTokenPath)

	def attemptSpotifyOAuthAndRetryImport(self, oauthToken=None):
		if oauthToken is None:
			return self.getOAuthTokenAndRetry()
		else:
			self.authedImporter = FinallySpotifyAuthedImporter(oauthToken)
			return self.importLibrary()

	def getOAuthTokenAndRetry(self):
		self.unauthedImporter = FinallySpotifyUnauthedImporter(self.oauthTokenPath)
		oauthToken = self.unauthedImporter.importLibrary()
		return self.attemptSpotifyOAuthAndRetryImport(oauthToken)

class FinallySpotifyUnauthedImporter(FinallySubimporter):
	oauthTokenPath = None

	def __init__(self, oauthTokenPath):
		self.oauthTokenPath = oauthTokenPath

	def sendSpotifyOAuthEndpoint(self):
		spotifyURL = self.spotifyAPIURL()
		spotifyEndpoint = self.spotifyEndpointPath()
		spotifyParams = self.spotifyEndpointParams()
		requestURLResponse = requests.get('https://'+spotifyURL+spotifyEndpoint, params=spotifyParams)
		requestURL = requestURLResponse.url
		print "\nOpening " + requestURL + "..."
		webbrowser.open(requestURL, new=2)

	def spotifyAPIURL(self):
		return "accounts.spotify.com"

	def spotifyEndpointPath(self):
		return "/authorize/"

	def spotifyOAuthClientID(self):
		return "2bbd8ddd581d44eebbd0d7f0a42c33d2"

	def spotifyOAuthRedirectURI(self):
		return "http://127.0.0.1:5000/spotify"

	def spotifyOAuthScope(self):
		return "user-library-read"

	def spotifyOAuthResponseType(self):
		return "code"

	def spotifyEndpointHeaders(self):
		return {"Content-Type" : "application/x-www-form-urlencoded"}

	def spotifyEndpointParams(self):
		params = {"client_id" : self.spotifyOAuthClientID(), "response_type" : self.spotifyOAuthResponseType(), "redirect_uri" : self.spotifyOAuthRedirectURI(), "scope" : self.spotifyOAuthScope()}
		return urllib.urlencode(params)

	def getSavedOAuthToken(self):
		tokenPathDir = self.oauthTokenPath.split(os.path.sep)[0]
		oauthTokenImporter = FinallyImporter(tokenPathDir)
		spotifyOAuthFilename = self.oauthTokenPath
		if oauthTokenImporter.checkFileExists(spotifyOAuthFilename) is True:
			contentsOfOAuthFile = oauthTokenImporter.getContentsOfFilePath(spotifyOAuthFilename)
			print "\nRead contents of OAuth file = " + str(contentsOfOAuthFile)
			return 
		else:
			return None

	def importLibrary(self):
		return self.attemptToImportLibrary(5)

	def attemptToImportLibrary(self, attempts):
		savedToken = self.getSavedOAuthToken()
		if savedToken is None:
			if attempts <= 0:
				raise ValueError("No more attempts!")
			else:
				self.sendSpotifyOAuthEndpoint()
				time.sleep(5)
				return self.attemptToImportLibrary(attempts-1)
		else:
			return savedToken

class FinallySpotifyAuthedImporter(FinallySubimporter):
	initialOffset = None
	limit = None
	authToken = None

	def __init__(self, authToken, initialOffset=0, limit=50):
		if authToken is None:
			raise ValueError("FinallySpotifyImporter requires authToken")

		self.authToken = authToken
		self.initialOffset = initialOffset
		self.limit = limit

	def spotifyAPIURL(self):
		return "api.spotify.com"

	def spotifyEndpointPath(self):
		return "/v1/me/tracks/"

	def spotifyEndpointHeaders(self):
		authHeaderValue = "Bearer " + self.authToken
		return {"Accept" : "application/json", "Content-Type" : "application/json", "Authorization" : authHeaderValue}

	def spotifyEndpointParams(self, offset):
		params = {"limit" : self.limit, "offset" : offset}
		return urllib.urlencode(params)

	def sendSpotifyTracksEndpoint(self, offset):
		spotifyURL = self.spotifyAPIURL()
		spotifyEndpoint = self.spotifyEndpointPath()
		spotifyParams = self.spotifyEndpointParams(offset)
		spotifyHeaders = self.spotifyEndpointHeaders()

		print "\nSending tracks endpoint w spotifyURL = " + str(spotifyURL) + " endpoint = " + str(spotifyEndpoint) + " params = " + str(spotifyParams) + " headers = " + str(spotifyHeaders)

		spotifyAPIConnection = httplib.HTTPSConnection(spotifyURL)
		spotifyAPIConnection.request("GET", spotifyEndpoint, {}, spotifyHeaders)
		spotifyAPIResponse = spotifyAPIConnection.getresponse()
		spotifyData = spotifyAPIResponse.read()

		jsonLoad = json.loads(spotifyData)
		try:
			error = jsonLoad["error"]["status"]
			print "\nExisting OAuth token " + str(self.authToken) + " invalid, trying to get a new one... error = " + str(error)
			return None
		except Exception, e:
			return spotifyData

	def importLibrary(self):
		return self.sendSpotifyTracksEndpoint(self.initialOffset)


if __name__ == "__main__":
	i = FinallySpotifyImporter()
	print "\n\n\n" + i.importLibrary()