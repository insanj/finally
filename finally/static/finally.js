
class FinallySong {
    constructor(origin, name, artist, album, duration) {
        this.origin = origin;
        this.name = name;
        this.artist = artist;
        this.album = album;
        this.duration = duration;
    }

    formattedDuration() {
    	var totalMinutes = (this.duration / 1000.0) / 60.0;
    	var wholeNumberMinutes = parseInt(totalMinutes);
    	var remainderMinutes = totalMinutes - wholeNumberMinutes;
    	var seconds = remainderMinutes * 60.0;
    	var wholeNumberSeconds = parseInt(seconds);

    	var minutesString = "";
    	if (wholeNumberMinutes < 10) {
    		minutesString = "0" + wholeNumberMinutes;
    	} else {
    		minutesString = wholeNumberMinutes;
    	}

    	var secondsString = "";
    	if (wholeNumberSeconds < 10) {
    		secondsString = "0" + wholeNumberSeconds;
    	} else {
    		secondsString = wholeNumberSeconds;
    	}

    	return minutesString + ":" + secondsString;
    }

    generateDiv() {
    	var originDiv;
    	if (this.origin == "spotify") {
			originDiv = "<img class='song-origin' id='spotify' src='static/spotify.jpg' />";
    	} else if (this.origin == "itunes") {
			originDiv = "<img class='song-origin' id='itunes' src='static/itunes.png' />";
    	} else {
    		originDiv = "<img class='song-origin' id='unknown' src='static/drum.png' />";
    	}

    	var nameDiv = "<div class='song-name'>" + this.name + "</div>";
    	var artistDiv = "<div class='song-artist'>" + this.artist + "</div>";
    	var albumDiv = "<div class='song-album'>" + this.album + "</div>";
    	var durationDiv = "<div class='song-duration'>" + this.formattedDuration() + "</div>";
    	var combinedDiv = originDiv + nameDiv + artistDiv + albumDiv + durationDiv;
        return "<div class='song'>" + combinedDiv + "</div>";
    }
}

class FinallyFrontend {
	constructor(alertDivSelector, parentDivSelector) {
		this.alertDivSelector = alertDivSelector;
		this.parentDivSelector = parentDivSelector;
	}

	sortedSongList(songList) {
		return songList.sort(function(a, b) {
	    	if (a.origin == null) {
	    		return b;
	    	} else if (b.origin == null) {
	    		return a;
	    	} else if (a.origin === b.origin) {
	    		if (a.artist == null) {
	    			return b;
	    		} else if (b.artist == null) {
	    			return a;
	    		} else {
	    			return a.artist.toLowerCase() > b.artist.toLowerCase();
	    		}
	    	} else {
	    		return a.origin.toLowerCase() > b.origin.toLowerCase();
	    	}
	    });
	}

	generateSongsFromJSONData(jsonData, maxPageSize) {
		$(this.alertDivSelector).text("🥁 Rendering JSON data...");
	    var reasonable;
	    if (maxPageSize < 0) {
	    	reasonable = jsonData;
	    } else {
	    	reasonable = jsonData.slice(0, maxPageSize);
	    }
	    var songs = [];
	    for (var i = 0; i < reasonable.length; i++) {
	        $(this.alertDivSelector).text("🥁 Parsing song " + i + "/" + reasonable.length);
	        var songJSON = reasonable[i];
	        var songParsedJSON = {};
	        try {
	            songParsedJSON = $.parseJSON(songJSON);
	        } catch(err) {
	            console.log(err)
	        }

	        var originId = songParsedJSON.origin.identifier;
		    var metadata = songParsedJSON.finallyMetadata;
		    var song = new FinallySong(originId, metadata.name, metadata.artist, metadata.album, metadata.duration);

		    songs.push(song);
	    }

	    var sortedSongs = this.sortedSongList(songs);
	    return sortedSongs;
	}

	generateDivsFromSongs(songs) {
	    // $(this.alertDivSelector).text("🥁 Sorting " + reasonable.length + " songs...");
	    // var sortedSongs = self.sortedSongList(songs);

	    $(this.alertDivSelector).text("🥁 Generating graphics, then we're done");
	    var generatedDivs = [];
	    for (var i = 0; i < songs.length; i++) {
	    	generatedDivs.push(songs[i].generateDiv());
	    }

	    return generatedDivs;
	}

	renderDivs(renderableDivs) {
	    $(this.parentDivSelector).empty();
	    for (var i = 0; i < renderableDivs.length; i++) {
	        $(this.parentDivSelector).append(renderableDivs[i]);
	    }
	}
}

class FinallyBackend {
	ajaxLoadJSONImportedData(completionBlock) {
	    $("#alert").text("🥁 Loading data...");
	    $.getJSON("/load", function(data) {
	        $("#alert").text("🥁 Finished downloading, importing...");
	        completionBlock(data);
	    }).fail(function(jqXHR, textStatus) {
	        $("#alert").text("⚠ Error downloading!");
	        completionBlock(null);
	    });
	}

	ajaxRunJSONImport(completionBlock) {
	    $("#alert").text("🥁 Re-importing data...");
	    $.getJSON("/run", function(data) {
	        $("#alert").text("🥁 Finished downloading, importing...");
	        completionBlock(data);
	    }).fail(function(jqXHR, textStatus) {
	        $("#alert").text("⚠ Error downloading!");
	        completionBlock(null);
	    });
	}
}