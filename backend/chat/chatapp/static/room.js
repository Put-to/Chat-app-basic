console.log("Sanity check from room.js.");

const roomName = localStorage.getItem("sessionID");
let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");

chatMessageInput.focus();

chatMessageInput.onkeyup = function (e) {
  if (e.keyCode === 13) {
    chatMessageSend.click();
  }
};

function displayMessage(text, color, alignment) {
  const messageDiv = document.createElement("div");
  messageDiv.style.color = color;
  messageDiv.style.textAlign = alignment;
  messageDiv.textContent = text;

  chatLog.appendChild(messageDiv);
  chatLog.scrollTop = chatLog.scrollHeight;
}

chatMessageSend.onclick = function () {
  if (chatMessageInput.value.length === 0) return;
  chatSocket.send(
    JSON.stringify({
      message: chatMessageInput.value,
    })
  );
  console.log(chatMessageInput.value);

  chatMessageInput.value = "";
};
let chatSocket = null;

function connect() {
  chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/connect/"
  );

  chatSocket.onopen = function (e) {
    console.log("Successfully connected to the WebSocket.");
  };

  chatSocket.onclose = function (e) {
    if (e.code === 4020) {
      displayMessage("Stranger Disconnected.", "red", "center");
    } else {
      setTimeout(function () {
        console.log("Reconnecting...");
        connect();
      }, 2000);
    }
  };

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);

    switch (data.type) {
      case "chat_message":
        if (data.user_id === roomName) {
          displayMessage("You: " + data.message, "black", "left");
        } else {
          displayMessage("Stranger: " + data.message, "black", "right");
        }
        break;
      case "connect":
        displayMessage(data.message, "green", "center");
        break;
      default:
        console.error("Unknown message type!");
        console.log(data);
        break;
    }

    chatLog.scrollTop = chatLog.scrollHeight;
  };

  chatSocket.onerror = function (err) {
    console.log("WebSocket encountered an error: " + err.message);
    console.log("Trying for now");
  };
}

connect();
