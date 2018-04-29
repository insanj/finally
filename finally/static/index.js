/* Requires finally.js */

function loadFinally() {
    $("#alert").text("🥁 Welcome!");

    var backend = new FinallyBackend();
    backend.ajaxLoadJSONImportedData(function(importedData){
        var frontend = new FinallyFrontend("#alert", "body");
        frontend.renderFinallyData(importedData);
    });
}
