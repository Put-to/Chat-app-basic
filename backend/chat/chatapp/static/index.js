console.log("Sanity check from index.js.");
var roomName = localStorage.getItem("sessionID");
// redirect to '/room/<roomInput>/'
document.querySelector("#roomConnect").onclick = function () {
  window.location.pathname = "chat/connect/";
};
