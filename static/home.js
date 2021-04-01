const chat = document.querySelector(".textarea");
const input = document.querySelector("input");
const form = document.getElementsByTagName("form")[0];
const logout = document.getElementsByTagName('a')[2];

const ADDRESS = "http://127.0.0.1/5000";

  var socket = io.connect()
  var name = null 
  socket.on('connect', async function(){
    name = await load_name();
    socket.emit('event', {
      name: name+ " ", 
      message: "has entered the chat",
    })

    form.onsubmit = async function (e){
      e.preventDefault();
      var msg = input.value;
      if (msg === "")
        return false;
      input.value = "";
      
      socket.emit('event',{
        name: name+ ": ",
        message: msg,
      });
    }
  })

  socket.on('message response', async function(msg){
    await display_message(msg);
  })

  window.onload = async function (){
    new_messages = await load_messages();
    new_messages.forEach(msg => display_message(msg));
  }

  logout.onclick = function() {
    socket.emit('event',{
      name: name,
      message: " has left the chat ",
    });
    socket.disconnect();
  }

async function load_name(){
    return  await fetch('/get_name')
    .then(async function (response) {
      return await response.json();
    }).then(function (text) {
        return text["name"];
    });
 }

async function load_messages(){
  return await fetch("/get_messages")
  .then(async function (response){
    return await response.json();
  })
  .then(function (text){
    return text["messages"];
  });
}

async function display_message(msg){
  console.log(msg)
  message_to_show = msg["name"] + msg["message"];
  let p = document.createElement('P');
  p.innerHTML = message_to_show;
  p.classList.add("chat-bubble");
  chat.appendChild(p);
}


function update_scroll(){
  if (!scrolled){
    chat.scrollTop = chat.scrollHeight;
  }
}

// $(function() {
//   $('#sendBtn').on('click', function(e) {
//   var msg = input.value;

//   input.value = "";
//   //   e.preventDefault()
//     $.getJSON('/run',
//       {message:msg},
//         function(data) {
//     });

//     return false;
//   });
// });

// function update(){

