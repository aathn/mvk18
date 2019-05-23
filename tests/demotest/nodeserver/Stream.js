var WebSocket = require("ws");

/* A Stream  */
class Stream {
  /**
   * Create a Stream with name, port and socket server
   * @param {string} streamName the name of the stream
   * @param {number} socketPort the port of the socket server
   */
  constructor(streamName, socketPort) {
    this.name = streamName;
    this.port = socketPort;
    this.socketServer = this.createSocketServer(socketPort);
    this.connectionCount = 0;
    console.log("Created socket server on port " + socketPort);
  }

  /**
   * Create a Socket server for stream running on port specified
   * @param {number} port the port number
   */
  createSocketServer(port) {
    let socketServer = new WebSocket.Server({
      port: port,
      perMessageDeflate: false
    });

    socketServer.on(
      "connection",
      function(socket, upgradeReq) {
        this.connectionCount++;
        console.log(
          "New WebSocket Connection: ",
          (upgradeReq || socket.upgradeReq).socket.remoteAddress,
          (upgradeReq || socket.upgradeReq).headers["user-agent"],
          "(" + this.connectionCount + " total)"
        );
        socket.on(
          "close",
          function(code, message) {
            this.connectionCount--;
            console.log(
              "Disconnected WebSocket (" + this.connectionCount + " total)"
            );
          }.bind(this)
        );
      }.bind(this)
    );

    socketServer.broadcast = function(data) {
      socketServer.clients.forEach(function each(client) {
        if (client.readyState === WebSocket.OPEN) {
          client.send(data);
        }
      });
    }.bind(socketServer);

    return socketServer;
  }
}

module.exports = Stream;
