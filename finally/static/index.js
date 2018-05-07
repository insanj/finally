/* Requires finally.js */
var finally_loadedSongs = [];
var finally_currentIndex = -1;
var finally_defaultPageSize = 500;

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
	var headerButtonTray = '<div id="button-tray">';
	headerButtonTray += '<div id="back-button">Back</div>';
	headerButtonTray += '<div id="page-indicator"></div>';
	headerButtonTray += '<div id="next-button">Next</div>';
	headerButtonTray += "</div>";

	var headerString = '<div id="header">';
	headerString += "<div id='header-body'></div>";
	headerString += headerButtonTray;
	headerString += "</div>";
	return headerString;
}

function renderFinally(data) {
    $("#loading").remove();
    $("#alert").text("");

	var headerDivString = generateHeaderDivString();
    $("body").append(headerDivString);

    finally_loadedSongs = generateTabulatorDataFromSongs(data);
    finally_currentIndex = 0;
    renderFinallySongs(finally_currentIndex, finally_defaultPageSize);
    renderFinallyLibraryMetadata(finally_loadedSongs, "header-body");
}

//

function generateTabulatorDataFromSongs(songsData) {
	var tabulatorSongs = songsData.map((v, i, a) => generateTabulatorDictFromSong(v, i));
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

function createFinallyServerMetadataDivs() {
	
}

//


function renderFinallyLibraryMetadata(metadataSongs, parentDivID) {
	var generatedDivs = createFinallyLibraryMetadataDivs(metadataSongs);
	var parentDivIDHash = "#"+parentDivID;
	$(parentDivIDHash).append("<div id='masthead'>🥁<br/>finally library</div>");
	for (var i = 0; i < generatedDivs.length; i++) {
		var g = generatedDivs[i];
		$(parentDivIDHash).append(g);
	}
}

function createFinallyLibraryMetadataDivs(metadataSongs) {
	var finallyTotalSongs = metadataSongs.length;
	var totalSongsDiv = generateFinallyLibraryMetadataDiv({"id" : "total-songs"}, "Total Songs: " + finallyTotalSongs);

	var finallyOnlySongs = metadataSongs.map(a => a.name);
	var finallyTotalSongsOnly = finallyOnlySongs.filter((v, i, a) => a.indexOf(v) === i).length; 
	var finallyTotalSongsOnlyDiv = generateFinallyLibraryMetadataDiv({"id" : "total-songs-only"}, "Total Songs (unique): " + finallyTotalSongsOnly);

	var finallyOnlyArtists = metadataSongs.map(a => a.artist);
	var finallyTotalArtists = finallyOnlyArtists.filter((v, i, a) => a.indexOf(v) === i).length; 
	var finallyTotalArtistsDiv = generateFinallyLibraryMetadataDiv({"id" : "total-artists"}, "Total Artists: " + finallyTotalArtists);

	var finallyOnlyAlbums = metadataSongs.map(a => a.album);
	var finallyTotalAlbums = finallyOnlyAlbums.filter((v, i, a) => a.indexOf(v) === i).length; 
	var finallyTotalAlbumsDiv = generateFinallyLibraryMetadataDiv({"id" : "total-albums"}, "Total Albums: " + finallyTotalAlbums);

	var finallyTotalDuration;

	var finallyTotalSpotifySongs = metadataSongs.filter(a => a.origin == "spotify").length;
	var finallyTotalSpotifySongsDiv = generateFinallyLibraryMetadataDiv({"id" : "spotify-songs"}, "Spotify Songs: " + finallyTotalSpotifySongs);

	var finallyTotaliTunesSongs = metadataSongs.filter(a => a.origin == "itunes").length;
	var finallyTotaliTunesSongsDiv = generateFinallyLibraryMetadataDiv({"id" : "itunes-songs"}, "iTunes Songs: " + finallyTotaliTunesSongs);

	var generatedDivs = [totalSongsDiv, finallyTotalSongsOnlyDiv, finallyTotalArtistsDiv, finallyTotalAlbumsDiv, finallyTotalSpotifySongsDiv, finallyTotaliTunesSongsDiv];
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
	var bodyParentDivID = "finally-body";
	var bodyParentDivIDHash = "#"+bodyParentDivID;
	$("body").append("<div id='"+bodyParentDivID+"'></div>");

	$("#page-indicator").text(beginIndex);
	$("#songs-table").remove();
    $(bodyParentDivIDHash).append('<div id="songs-table"></div>');

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