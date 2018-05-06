/* Requires finally.js */
var finally_loadedSongs = [];
var finally_currentIndex = -1;
var finally_defaultPageSize = 100;

function runAndLoadFinally() {
    $("#alert").text("🥁 Welcome!");

    var backend = new FinallyBackend();
    backend.ajaxRunJSONImport(function(importedData) {
        var frontend = new FinallyFrontend("#alert", "body");
        var frontendData = frontend.generateSongsFromJSONData(importedData, -1);
		renderFinally(frontendData);
    });
}

function loadFinally() {
    $("#alert").text("🥁 Welcome!");

    var backend = new FinallyBackend();
    backend.ajaxLoadJSONImportedData(function(importedData) {
    	if (importedData.hasOwnProperty("error")) {
    		console.log("🤨 No Finally JSON library file found? Running from scratch... " + importedData);
    		runAndLoadFinally();
    	} else {
    		var frontend = new FinallyFrontend("#alert", "body");
        	var frontendData = frontend.generateSongsFromJSONData(importedData, -1);
			renderFinally(frontendData);
    	}
    });
}

function generateHeaderDivString() {
	var headerString = '<div id="header">';
	headerString += '<div id="back-button">Back</div>';
	headerString += '<div id="page-indicator"></div>';
	headerString += '<div id="next-button">Next</div>';
	headerString += "</div>";
	return headerString;
}

function renderFinally(data) {
    $("#loading").remove();
    $("#alert").text("🥁");

	var headerDivString = generateHeaderDivString();
    $("body").append(headerDivString);

    finally_loadedSongs = generateTabulatorDataFromSongs(data);
    finally_currentIndex = 0;
    renderFinallySongs(finally_currentIndex, finally_defaultPageSize);
    renderFinallyLibraryMetadata(finally_loadedSongs, "header");
}

//

function generateTabulatorDataFromSongs(songsData) {
	var tabulatorSongs = [];
	for (var i = 0; i < songsData.length; i++) {
    	var tabulatorConvertedSong = generateTabulatorDictFromSong(songsData[i], i);
    	tabulatorSongs.push(tabulatorConvertedSong);
    }

	return tabulatorSongs;
}

function generateTabulatorDictFromSong(song, i) {
	var tabulatorDict = {};
	tabulatorDict["id"] = i;
	tabulatorDict["name"] = song.name;
	tabulatorDict["artist"] = song.artist;
	tabulatorDict["album"] = song.album;
	tabulatorDict["duration"] = song.duration;
	tabulatorDict["origin"] = song.origin;
	return tabulatorDict;
}

// 


function renderFinallyLibraryMetadata(metadataSongs, parentDivID) {
	var generatedDivs = createFinallyLibraryMetadataDivs(metadataSongs);
	var parentDivIDHash = "#"+parentDivID;
	for (var i = 0; i < generatedDivs.length; i++) {
		var g = generatedDivs[i];
		$(parentDivIDHash).append(g);
	}
}

function createFinallyLibraryMetadataDivs(metadataSongs) {
	var finallyTotalSongs = metadataSongs.length;
	var totalSongsDiv = generateFinallyLibraryMetadataDiv({"id" : "total-songs"}, "Total Songs: " + finallyTotalSongs);

	var finallyTotalArtists;
	
	var finallyTotalAlbums;
	var finallyTotalDuration;
	var finallyTotalSpotifySongs;
	var finallyTotaliTunesSongs;
	var finallyTotalSongs;

	var generatedDivs = [totalSongsDiv];
	return generatedDivs;
}

function generateFinallyLibraryMetadataDiv(elementInfo, elementContents) {
	var divInFlight = "<div ";
	for (var i = 0; i < elementInfo.length; i++) {
		var e = elementInfo[i];
		var divString = e["key"] + "=" + e["value"];
		divInFlight += divString;
	}

	divInFlight += ">";
	divInFlight += elementContents;
	divInFlight += "</div>";
	return divInFlight;
}

//

function renderFinallySongs(beginIndex, pageSize) {
	$("#page-indicator").text(beginIndex);
	$("#songs-table").remove();
    $("body").append('<div id="songs-table"></div>');

	var slicedSongs = finally_loadedSongs.slice(beginIndex, pageSize);
    $("#songs-table").tabulator({
		layout:"fitColumns",
    	data: slicedSongs,
	    columns:[
	        {title:"name", field:"name"},
	        {title:"artist", field:"artist"},
	        {title:"album", field:"album"},
	        {title:"origin", field:"origin"},
	        {title:"duration", field:"duration", sorter:"number"},
	    ],
	});
}

$("body").on("click", "#back-button",  function(e) {
	e.preventDefault();
	finally_currentIndex = finally_currentIndex - finally_defaultPageSize;

	if (finally_currentIndex >= 0) {
		renderFinallySongs(finally_currentIndex, finally_currentIndex+finally_defaultPageSize);
	} else {
		finally_currentIndex = -1;
	}
});

$("body").on("click", "#next-button",  function(e) {
	e.preventDefault();
	finally_currentIndex = finally_currentIndex + finally_defaultPageSize;

	if (finally_currentIndex < finally_loadedSongs.length) {
		renderFinallySongs(finally_currentIndex, finally_currentIndex+finally_defaultPageSize);
	} else {
		finally_currentIndex = finally_loadedSongs.length;
	}
});