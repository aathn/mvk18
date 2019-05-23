var WebSocket = require("ws"),
  Stream = require("./Stream");

/* Configurations */
const MIN_PORT_NUMBER = 3000;
const MAX_PORT_NUMBER = 4000;

/** A Class that handles all current streams and their socket servers. */
class StreamHandler {
  /**
   * Create a StreamHandler.
   */
  constructor() {
    this.activeStreamPorts = [];
    this.activeStreams = {};
  }

  /** Initialize and add a stream
   * @param {string} name - the naming of the new stream
   */
  addStream(name) {
    console.log("Adding stream");
    // Find a port and create the stream (with socket server)
    let port = this.getFreePort();
    if (port) {
      let newStream = new Stream(name, port);
      this.activeStreams[name] = newStream;
      return true;
    } else {
      console.log("Error! No free ports were found!");
      return false;
    }
  }

  /** Remove a stream, close its socket server and free its port
   * @param {string} name - the naming of the stream to close
   * @return {bool} true if the stream was removed.
   */
  closeStream(name) {
    // Stop the socket server and free the port + name
    let currentStream = this.getStream(name);
    if (currentStream) {
      currentStream.socketServer.close();
      this.activeStreamPorts[currentStream.port] = false;
      delete this.activeStreams[name];
      return true;
    }
    return false;
  }

  /** Get the lowest open port in range MIN_PORT_NUMBER <= return value <= MAX_PORT_NUMBER
   * if it does exist, else return 0
   * @return {number} the free port that was found or 0
   */
  getFreePort() {
    for (let i = MIN_PORT_NUMBER; i <= MAX_PORT_NUMBER; i++) {
      if (!this.activeStreamPorts[i]) {
        this.activeStreamPorts[i] = true;
        return i;
      }
    }
    return 0;
  }

  /** Get the port of a streams socket server.
   * @param {string} name - The name of the stream which port to get
   * @return {number} the port or 0 if stream was not found
   */
  getStreamPort(name) {
    // Get a port of a stream
    let currentStream = this.getStream(name);
    if (currentStream) {
      return currentStream.port;
    }
    return 0;
  }

  /** Get the Stream Object for a stream of specified name.
   * @param {string} name - The name of the stream to get
   * @return {Stream} the stream or 0 if stream was not found
   */
  getStream(name) {
    if (!this.activeStreams[name]) {
      return false;
    } else {
      return this.activeStreams[name];
    }
  }

  /** Get all stream objects
   * @return {Object(Stream)} an object with all active stream objects
   */
  get allStreams() {
    return this.activeStreams;
  }
}

module.exports = StreamHandler;
