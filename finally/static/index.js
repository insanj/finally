
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

function renderFinallyData(json) {
    var songs = [];
    for (var i = 0; i < json.length; i++) {
        var songJSON = json[i];
        var songParsedJSON = $.parseJSON(songJSON);

        var name = songParsedJSON.name;
        var identifier = songParsedJSON.identifier;
        var origin = songParsedJSON.origin;

        var song = new FinallySong(origin, name, identifier);
        songs.push(song);
    }

    var sortedSongs = songs.sort(function(a, b) {
        return b.name-a.name;
    });;

    $("body").empty();
    for (var i = 0; i < sortedSongs.length; i++) {
        var div = sortedSongs[i].generateDiv();
        $("body").append(div);
    }
}

function runFinallyPython(completionBlock) {
    var phraseAPIURL = "/run"
    $.get(phraseAPIURL, function(data) {
        console.log(data)
        completionBlock(data);
    }).fail(function(jqXHR, textStatus) {
        console.log(textStatus);
        completionBlock(null);
    });
}

function loadFinally() {
    runFinallyPython(function(result) {
        if (result == null) {
            console.log("⚠ result == null");
            return;
        }

        renderFinallyData(result);
    });
}
