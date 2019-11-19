const RSA = require('./index.js');
require('./reconnecting-websocket.js');

var chatSocket = new ReconnectingWebSocket(
    'ws://' + window.location.host +
    '/ws/chat/' + roomName + '/');

chatSocket.onopen = function(e) {
  fetchMessages();
}

chatSocket.onmessage = function(e) {
  var data = JSON.parse(e.data);
  if (data['command'] === 'new_message'){
    createMessage(data['message']);
  }
  else if (data['command'] === 'messages'){
    for (let i = 0; i < data['messages'].length; i++){
      createMessage(data['messages'][i]);
    }
  }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    var messageInputDom = document.querySelector('#chat-message-input');
    var message = messageInputDom.value;

    const string_message = JSON.stringify({
      'message': message,
      'from': username,
      'command': 'new_message',
    });

    const encoded_message = RSA.encode(string_message);
    // These are the 'n' and 'e' public values that you need to encrypt the message
    const encrypted_message = RSA.encrypt(encoded_message, server_public_key , 65537);
    console.log("KEYS : n -> " + server_public_key + " ; e -> 65537");
    chatSocket.send(encrypted_message);
    console.log(encrypted_message);
    console.log(typeof(encrypted_message));

    messageInputDom.value = '';
};

function fetchMessages() {
  chatSocket.send(JSON.stringify({'command': 'fetch_messages'}));
}

function createMessage(message) {
  var content = message['content'];
  var time = message['timestamp'];
  var author = message['author'];
  var  msg_to_print = "[" + time + "]" + author + ":" + content;
  document.querySelector('#chat-log').value += (msg_to_print + '\n');
}
