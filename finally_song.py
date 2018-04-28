#!/usr/bin/python

class FinallySongOrigin:
	identifier = None
	timestamp = None
	def __init__(self, identifier, timestamp):
		if identifier not in validIdentifiers:
			raise ValueError("[FinallySongOrigin] invalid identifier") 

		self.identifier = identifier
		self.timestamp = timestamp

	@classmethod
	def spotifyIdentifier():
		return "spotify"

	@classmethod
	def itunesIdentifier():
		return "itunes"

	@classmethod
	def validIdentifiers():
		return [FinallySongOrigin.spotifyIdentifier(), FinallySongOrigin.itunesIdentifier()]


class FinallySong:
	origin = None
	def __init__(self, origin):
		self.origin = origin

	songOrigin
	songTrackID = None
	songName
	songArtist
	songAlbumArtist
	songAlbum
	songGenre
	songKind
	songSize
	songTotalTime
	songDiscNumber


			<key>Track ID</key><integer>5091</integer>
			<key>Name</key><string>Day 6</string>
			<key>Artist</key><string>Ta-ku</string>
			<key>Album Artist</key><string>Ta-ku</string>
			<key>Album</key><string>50 Days For Dilla, Vol. 1</string>
			<key>Genre</key><string>Hip Hop/Rap</string>
			<key>Kind</key><string>Apple Music AAC audio file</string>
			<key>Size</key><integer>4015138</integer>
			<key>Total Time</key><integer>107833</integer>
			<key>Disc Number</key><integer>1</integer>
			<key>Disc Count</key><integer>1</integer>
			<key>Track Number</key><integer>6</integer>
			<key>Track Count</key><integer>25</integer>
			<key>Year</key><integer>2012</integer>
			<key>Date Modified</key><date>2016-02-08T18:25:45Z</date>
			<key>Date Added</key><date>2016-02-08T18:25:45Z</date>
			<key>Bit Rate</key><integer>256</integer>
			<key>Sample Rate</key><integer>44100</integer>
			<key>Artwork Count</key><integer>1</integer>
			<key>Sort Album</key><string>50 Days For Dilla, Vol. 1</string>
			<key>Sort Artist</key><string>Ta-ku</string>
			<key>Sort Name</key><string>Day 6</string>
			<key>Persistent ID</key><string>B64F93B30A385723</string>
			<key>Track Type</key><string>Remote</string>
			<key>Apple Music</key><true/>