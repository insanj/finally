#!/usr/bin/python
import httplib, urllib
import webbrowser
import requests
import time
import base64
import json
from finally_importer import *

class FinallySubimporter:
	def importLibrary(self):
		raise ValueError("FinallySubimporter no-op must override importLibrary")	

class FinallySpotifyImporter(FinallySubimporter):
	oauthCodeFolderPath = None
	oauthCodeFilePath = None

	def __init__(self):
		self.oauthCodeFolderPath = os.path.join(os.getcwd(), "oauth")
		self.oauthCodeFilePath = os.path.join(self.oauthCodeFolderPath, "spotify.txt")

	def importLibrary(self):
		oauthCodeImporter = FinallySpotifyOAuthCodeImporter(self.oauthCodeFilePath)
		oauthCode = oauthCodeImporter.importLibrary()

		if oauthCode is None:
			raise ValueError("FinallySpotifyOAuthCodeImporter failed to get oauthCode")
		else:
			print "\nFinallySpotifyLibraryImporter oauthCode = " + str(oauthCode)

		oauthTokenImporter = FinallySpotifyOAuthTokenImporter(oauthCode)
		oauthToken = oauthTokenImporter.importLibrary()

		if oauthToken is None:
			print "\nFinallySpotifyLibraryImporter deleting existing oauth code and trying again"
			oauthCodeImporter.deleteExistingOAuthCode() # invalid code probs
			return self.importLibrary() # gross
		else:
			print "\nFinallySpotifyLibraryImporter oauthToken = " + str(oauthToken)

		authedImporter = FinallySpotifyLibraryImporter(oauthToken)
		authedLibrary = authedImporter.importLibrary()

		if authedLibrary is None:
			raise ValueError("FinallySpotifyLibraryImporter failed to get authedLibrary")
		else:
			print "\nFinallySpotifyLibraryImporter authedLibrary complete!"

		return authedLibrary

class FinallySpotifyOAuthCodeImporter(FinallySubimporter):
	oauthCodePath = None

	def __init__(self, oauthCodePath):
		self.oauthCodePath = oauthCodePath

	def deleteExistingOAuthCode(self):
		os.remove(self.oauthCodePath)

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

	def importLibrary(self):
		return self.attemptToImportLibrary(3)

	def attemptToImportLibrary(self, attempts):
		savedToken = self.getSavedOAuthCode()

		if savedToken is None:
			if attempts <= 0:
				raise ValueError("FinallySpotifyOAuthCodeImporter attemptToImportLibrary No more attempts!")
			else:
				self.sendSpotifyOAuthCodeEndpoint()
				time.sleep(2)
				return self.attemptToImportLibrary(attempts-1)
		else:
			return savedToken

	def getSavedOAuthCode(self):
		try:
			with open(self.oauthCodePath) as contents:
				return contents.read()
		except Exception, e:
			print "\nFinallySpotifyOAuthCodeImporter getSavedOAuthCode except = " + str(e)
			return None

	def sendSpotifyOAuthCodeEndpoint(self):
		spotifyURL = self.spotifyAPIURL()
		spotifyEndpoint = self.spotifyEndpointPath()
		spotifyParams = self.spotifyEndpointParams()
		requestURLResponse = requests.get('https://'+spotifyURL+spotifyEndpoint, params=spotifyParams)
		requestURL = requestURLResponse.url
		print "\nOpening " + requestURL + "..."
		webbrowser.open(requestURL, new=2)

class FinallySpotifyOAuthTokenImporter(FinallySubimporter):
	oauthCode = None

	def __init__(self, oauthCode):
		self.oauthCode = oauthCode

	def spotifyAPIURL(self):
		return "accounts.spotify.com"

	def spotifyEndpointPath(self):
		return "/api/token"

	def spotifyTokenGrantType(self):
		return "authorization_code"

	def spotifyOAuthRedirectURI(self):
		return "http://127.0.0.1:5000/spotify"

	def spotifyBase64EncodedClientCreds(self):
		return "MmJiZDhkZGQ1ODFkNDRlZWJiZDBkN2YwYTQyYzMzZDI6YjM3NGJhMTY4ZjFjNDNmYThkMjhkY2Q1MjY0Mzc2MjQ="

	def spotifyOAuthClientID(self):
		return "2bbd8ddd581d44eebbd0d7f0a42c33d2"

	def spotifyOAuthClientSecret(self):
		return "b374ba168f1c43fa8d28dcd526437624"

	def spotifyEndpointHeaders(self):
		authorizationHeaderString = "Basic " + self.spotifyBase64EncodedClientCreds()
		return {"Content-Type" : "application/x-www-form-urlencoded"}

	def spotifyEndpointParams(self):
		params = {"grant_type" : self.spotifyTokenGrantType(), "code" : self.oauthCode, "redirect_uri" : self.spotifyOAuthRedirectURI(), "client_id" : self.spotifyOAuthClientID(), "client_secret" : self.spotifyOAuthClientSecret()}
		return urllib.urlencode(params)

	def importLibrary(self):
		return self.sendSpotifyTokenEndpoint()

	def sendSpotifyTokenEndpoint(self):
		spotifyURL = self.spotifyAPIURL()
		spotifyEndpoint = self.spotifyEndpointPath()
		spotifyParams = self.spotifyEndpointParams()
		spotifyHeaders = self.spotifyEndpointHeaders()

		print "\nFinallySpotifyOAuthTokenImporter sendSpotifyTokenEndpoint Sending token endpoint w spotifyURL = " + str(spotifyURL) + " endpoint = " + str(spotifyEndpoint) + " params = " + str(spotifyParams) + " headers = " + str(spotifyHeaders)

		spotifyAPIConnection = httplib.HTTPSConnection(spotifyURL)
		spotifyAPIConnection.request("POST", spotifyEndpoint, spotifyParams, spotifyHeaders)
		spotifyAPIResponse = spotifyAPIConnection.getresponse()
		print "\nspotifyAPIResponse =" + str(spotifyAPIResponse.status) + ", " + str(spotifyAPIResponse.reason)

		spotifyData = spotifyAPIResponse.read()
		spotifyAPIConnection.close()

		print "\nFinallySpotifyOAuthTokenImporter sendSpotifyTokenEndpoint = " + str(spotifyData)
		jsonLoad = json.loads(spotifyData)

		try:
			error = jsonLoad["error"]
			print "\nToken request error = " + str(error)
			return None
		except Exception, e:
			print "\nToken request has no JSON error"
			try:
				return jsonLoad["access_token"]
			except Exception, e:
				print "\nToken request has no access_token??"
				return None

class FinallySpotifyLibraryImporter(FinallySubimporter):
	oauthToken = None
	attemptToRecurse = None

	def __init__(self, oauthToken, attemptToRecurse=True):
		self.oauthToken = oauthToken
		self.attemptToRecurse = attemptToRecurse

	def spotifyAPIURL(self):
		return "api.spotify.com"

	def spotifyEndpointPath(self):
		return "/v1/me/tracks/"

	def spotifyEndpointPathWithParams(self, limit, offset):
		return self.spotifyEndpointPath() + "?limit=" + str(limit) + "&offset=" + str(offset)

	def spotifyEndpointHeaders(self):
		authHeaderValue = "Bearer " + self.oauthToken
		return {"Accept" : "application/json", "Content-Type" : "application/x-www-form-urlencoded", "Authorization" : authHeaderValue}

	def singleSendSpotifyTracksEndpoint(self, u, e, h):
		print "\nFinallySpotifyLibraryImporter Sending tracks endpoint w spotifyURL = " + str(u) + " endpoint = " + str(e) + " headers = " + str(h)

		spotifyAPIConnection = httplib.HTTPSConnection(u)
		spotifyAPIConnection.request("GET", e, {}, h)
		spotifyAPIResponse = spotifyAPIConnection.getresponse()
		spotifyData = spotifyAPIResponse.read()
		spotifyAPIConnection.close()
		
		jsonLoad = None
		try:
			jsonLoad = json.loads(spotifyData)
			print "\nFinallySpotifyLibraryImporter singleSendSpotifyTracksEndpoint done = " + str(len(jsonLoad))
		except Exception, e:
			print "\nFinallySpotifyLibraryImporter error with json " + str(spotifyData) + " = " + str(e)
			return None

		try:
			error = jsonLoad["error"]["status"]
			print "\nFinallySpotifyLibraryImporter error = " + str(error)
			return None
		except Exception, e:
			return jsonLoad

	def sendSpotifyTracksEndpoint(self):
		spotifyURL = self.spotifyAPIURL()
		spotifyParams = self.spotifyParams()
		spotifyEndpoint = self.spotifyEndpointPath()
		spotifyHeaders = self.spotifyEndpointHeaders()
		return self.singleSendSpotifyTracksEndpoint(spotifyURL, spotifyEndpoint, spotifyHeaders, spotifyParams)

	def extractEndpointFromNextURL(self, nextURL):
		offsetValueBeginIndex = nextURL.find("offset=")
		offsetValueLength = len("offset=")
		offsetValueEndIndex = nextURL.find("&", offsetValueBeginIndex)
		if offsetValueEndIndex < 0:
			offsetValueEndIndex = len(nextURL)-1

		limitValueBeginIndex = nextURL.find("limit=")
		limitValueLength = len("limit=")
		limitValueEndIndex = nextURL.find("&", limitValueBeginIndex)
		if limitValueEndIndex < 0:
			limitValueEndIndex = len(nextURL)-1

		offsetValue = nextURL[offsetValueBeginIndex+offsetValueLength:offsetValueEndIndex+1]
		limitValue = nextURL[limitValueBeginIndex+limitValueLength:limitValueEndIndex+1]

		#offsetStr = str(offsetValue)
		#limitStr = str(limitValue)
		#params =  urllib.urlencode({"offset" : offsetStr, "limit" : limitStr})
		return self.spotifyEndpointPathWithParams(limitValue, offsetValue)

	def unrollRecursiveResults(self, results):
		if results is None:
			return None
		if len(results) is 1:
			return results[0]
		else:
			baseResult = results[0]
			baseItemsArray = baseResult["items"]
			for i in range(1, len(results)):
				subresult = results[i]
				try:
					subresultItems = subresult["items"]
					for subresultItem in subresultItems:
						baseItemsArray.append(subresultItem)
				except Exception, e:
					print "Unable to grab the items from subresult = " + str(subresult)
					print "unrollRecursiveResults e " + str(e)

			baseResult["items"] = baseItemsArray
			return baseResult

	def recursivelySendSpotifyTracksEndpoint(self, endpoint, foundResults=[]):
		spotifyURL = self.spotifyAPIURL()
		spotifyHeaders = self.spotifyEndpointHeaders()
		jsonResponse = self.singleSendSpotifyTracksEndpoint(spotifyURL, endpoint, spotifyHeaders)

		if jsonResponse is not None:
			foundResults.append(jsonResponse)

			try:
				nextURL = jsonResponse['next']
				if nextURL is None:
					return foundResults	
				else:
					print "\nFinallySpotifyLibraryImporter found next URL = " + str(nextURL) + " so far have " + str(len(foundResults))
					nextEndpoint = self.extractEndpointFromNextURL(nextURL)

					return self.recursivelySendSpotifyTracksEndpoint(nextEndpoint, foundResults)
			except Exception, e:
				print "\nFinallySpotifyLibraryImporter NO NEXT URL FOUND in = " + str(jsonResponse.keys()) + "\n error = " + str(e) 
				return foundResults
		else:
			return foundResults	

	def importLibrary(self):
		print "\nFinallySpotifyLibraryImporter beginning import, attemptToRecurse = " + str(self.attemptToRecurse)

		parsedJSONResponse = None
		if self.attemptToRecurse is True:
			recursiveResults = self.recursivelySendSpotifyTracksEndpoint(self.spotifyEndpointPathWithParams(50, 0))
			parsedJSONResponse = self.unrollRecursiveResults(recursiveResults)
		else:
			parsedJSONResponse = self.sendSpotifyTracksEndpoint()

		return json.dumps(parsedJSONResponse)

if __name__ == "__main__":
	i = FinallySpotifyImporter()
	print "\n\n\n" + i.importLibrary()