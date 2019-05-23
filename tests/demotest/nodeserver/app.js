/* Server to receive and serve mpeg streams being streamed from ffmpeg
- based on code from https://github.com/phoboslab/jsmpeg (MIT) */
var fs = require("fs"),
  StreamHandler = require("./StreamHandler");
var hbs = require("express-handlebars");
const express = require("express");
const os = require("os");

const WEB_SERVER_PORT = 80;
const WEB_SERVER_HOST = os.hostname();

/* Create the stream handler object, keeping track of all streams */
let streamHandler = new StreamHandler();

/* Receive server and web server (combined) */
const app = express();

/* User public folder with javascript, css and graphics */
app.use(express.static("public"));

/* Use handlebars as view engine, all templates are in the /views directory */
app.engine("handlebars", hbs({ defaultLayout: "main" }));
app.set("view engine", "handlebars");

/* Render front page */
app.get("/", function(req, res) {
  res.render("frontpage", { streams: streamHandler.allStreams, ip: req.get('host') });
});

/* Get a JSON object of all streams */
app.get("/api/streams", function(req, res) {
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(streamHandler.allStreams));
});

/* Receive stream contents */
app.post("/livestream/:name", receiveStream);

/* Start stream */
app.listen(WEB_SERVER_PORT, () =>
  console.log(`Web Server listening on ${WEB_SERVER_HOST}:${WEB_SERVER_PORT}!`)
);

/** Function used to receive streams from ffmpeg to the express server
 * @param {Object} request the express request object
 * @param {Object} response the express response object
 */
function receiveStream(request, response) {
  console.log("Starting");
  var streamName = request.params["name"];

  if (streamHandler.addStream(streamName)) {
    console.log("Creating stream for " + streamName);
  } else {
    console.log("Error adding stream " + streamName);
  }

  // Not sure why this is here, just copied from the example on github
  response.connection.setTimeout(0);
  // broadcast data to streams socket server
  request.on(
    "data",
    function(data) {
      streamHandler.getStream(streamName).socketServer.broadcast(data);
      if (request.socket.recording) {
        request.socket.recording.write(data);
      }
    }.bind(streamName)
  );
  // when the camera stops sending to stream
  request.on(
    "end",
    function() {
      console.log("close");
      // close the stream and recording
      streamHandler.closeStream(streamName);
      if (request.socket.recording) {
        request.socket.recording.close();
      }
    }.bind(streamName)
  );
}
