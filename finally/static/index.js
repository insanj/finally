/* Requires finally.js */

function loadFinally() {
    $("#alert").text("🥁 Welcome!");

    var backend = new FinallyBackend();
    backend.ajaxLoadJSONImportedData(function(importedData){
        var frontend = new FinallyFrontend("#alert", "body");
        var frontendData = frontend.generateSongsFromJSONData(importedData, -1);
        renderFinally(frontendData);
    });
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

function generateTabulatorDataFromSongs(songsData) {
	var tabulatorSongs = [];
	for (var i = 0; i < songsData.length; i++) {
    	var tabulatorConvertedSong = generateTabulatorDictFromSong(songsData[i], i);
    	tabulatorSongs.push(tabulatorConvertedSong);
    }

	return tabulatorSongs;
}

function renderFinally(data) {
    $("body").empty();
    $("body").append('<div id="songs-table"></div>');
    
    var tabulatorSongs = generateTabulatorDataFromSongs(data);
    $("#songs-table").tabulator({
    	data: tabulatorSongs,
	    height:"311px",
	    columns:[
	        {title:"name", field:"name"},
	        {title:"artist", field:"artist"},
	        {title:"album", field:"album"},
	        {title:"origin", field:"origin"},
	        {title:"duration", field:"duration", sorter:"number"},
	    ],
	});
}

/*
var songContainerID = "song-container";
$("body").append("<div id='"+songContainerID+"'></div>");
for (var i = 0; i < frontendDivs.length; i++) {
	$("#"+songContainerID).append(frontendDivs[i]);
}


$("#"+songContainerID).prepend('<input class="search" placeholder="Search" />');
$("#"+songContainerID).prepend('<button class="sort" data-sort="song-name">Sort by name</button>');  
$("#"+songContainerID).prepend('<ul class="pagination"></ul>');

var sortableDivsList = new List(songContainerID, {
	valueNames: ['song-name', 'song-artist', 'song-album', 'song-duration', 'song-origin'],
	page: 50,
	pagination: true
});*/