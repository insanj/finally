
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

function renderFinallyData(jsonData) {
    $("#alert").text("🥁 Rendering JSON data...");
    var reasonable = jsonData.slice(0, 5);
    var songs = [];
    for (var i = 0; i < reasonable.length; i++) {
        $("#alert").text("🥁 Rendering song " + i + "/" + reasonable.length);
        var songJSON = reasonable[i];
        var songParsedJSON = {};
        try {
            songParsedJSON = $.parseJSON(songJSON);
        } catch(err) {
            console.log(err)
        }

        var name = songParsedJSON.name;
        var identifier = songParsedJSON.identifier;
        var origin = songParsedJSON.origin;

        var song = new FinallySong(origin, name, identifier);
        songs.push(song);
    }

    $("#alert").text("🥁 Sorting, then see ya!");
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
    $("#alert").text("🥁 Loading data...");
    var phraseAPIURL = "/load"
    $.getJSON(phraseAPIURL, function(data) {
        $("#alert").text("🥁 Finished downloading, importing...");
        completionBlock(data);
    }).fail(function(jqXHR, textStatus) {
        $("#alert").text("⚠ Error downloading!");
        completionBlock(null);
    });
}

function loadFinally() {
    $("#alert").text("🥁 Welcome!");

    runFinallyPython(function(result) {
        if (result == null) {
            $("#alert").text("⚠ Unexpected error!");
            return;
        }

        renderFinallyData(result);
    });
}
