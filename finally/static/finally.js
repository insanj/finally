
class FinallySong {
    constructor(origin, name, identifier) {
        this.origin = origin;
        this.name = name;
        this.identifier = identifier;
    }

    generateDiv() {
        return "<div class='song'><div class='song-origin'>" + this.origin + "</div><div class='song-name'>" + this.name + "</div></div>";
    }
}

class FinallyFrontend {
	constructor(alertDivSelector, parentDivSelector) {
		this.alertDivSelector = alertDivSelector;
		this.parentDivSelector = parentDivSelector;
	}

	renderFinallyData(jsonData) {
	    $(this.alertDivSelector).text("🥁 Rendering JSON data...");
	    var reasonable = jsonData.slice(0, 5);
	    var songs = [];
	    for (var i = 0; i < reasonable.length; i++) {
	        $(this.alertDivSelector).text("🥁 Rendering song " + i + "/" + reasonable.length);
	        var songJSON = reasonable[i];
	        var songParsedJSON = {};
	        try {
	            songParsedJSON = $.parseJSON(songJSON);
	        } catch(err) {
	            console.log(err)
	        }

	        var originId = songParsedJSON.origin.identifier;
	        var metadata = $.parseJSON(songParsedJSON.metadata);
	        var song;
	        if (originId == "spotify") {
	            song = new FinallySong(originId, metadata.name, metadata.id);
	        } else {
	            song = new FinallySong(originId, metadata["Name"], metadata["Track ID"]);
	        }

	        songs.push(song);
	    }

	    $(this.alertDivSelector).text("🥁 Sorting, then see ya!");
	    var sortedSongs = songs.sort(function(a, b) {
	        return b.name-a.name;
	    });;

	    $(this.parentDivSelector).empty();
	    for (var i = 0; i < sortedSongs.length; i++) {
	        var div = sortedSongs[i].generateDiv();
	        $(this.parentDivSelector).append(div);
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