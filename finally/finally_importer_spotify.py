#!/usr/bin/python
import httplib, urllib

class FinallySpotifyImporter:
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

		spotifyAPIConnection = httplib.HTTPSConnection(spotifyURL)
		spotifyAPIConnection.request("GET", spotifyEndpoint, spotifyParams, spotifyHeaders)
		spotifyAPIResponse = spotifyAPIConnection.getresponse()
		spotifyData = spotifyAPIResponse.read()
		return spotifyData

	def getSpotifyLibrary(self):
		return self.sendSpotifyTracksEndpoint(self.initialOffset)


if __name__ == "__main__":
	julianAuthToken = "BQAj8hnxEC9fEKonoTUEEU4Sk0UH7UFwW4wsdXViL_bFufpRwpOw4mNQAQAkjFNJ8Qhl3Po7x2cQt1TMrdz0-mAWB-u8VAE5s_bzoFmCrD56RHVqEknWLAw4LAxYmfY_MEH2KlQVLMQyT0qp8w"
	spotifyImporter = FinallySpotifyImporter(julianAuthToken)
	print(spotifyImporter.getSpotifyLibrary())
