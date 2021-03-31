const chat = document.querySelector(".textarea");
const input = document.querySelector("input");
const form = document.getElementsByTagName("form")[0];


const ADDRESS = "http://127.0.0.1/5000";

let scrolled = false;

  var socket = io.connect()

  socket.on('connect', async function(){
    new_messages = await load_messages();
    new_messages.forEach(msg => display_message(msg));
    var name = await load_name();
    var msg = name + " has entered the chat ";
    socket.send(msg);

    // socket.on("disconnect", async function (msg) {
    //   var usr_name = await load_name();
    //   socket.emit("event", {
    //     message: usr_name + " just left the server...",
    //   });
    // });

  })

  window.onbeforeunload = async function () {
    console.log(3);
    var usr_name = await load_name();
    socket.emit('event', {
      message: usr_name + " just left the server...",
    });
}

window.onload = function(){


  form.onsubmit = async function (e){
    e.preventDefault();
    var msg = input.value;
    if (msg === "")
      return false;
    input.value = "";

    let user_name = await load_name();
    var message_to_show = user_name+": "+ msg;

    socket.send(message_to_show);
  }
  socket.on("message",function(msg){
      display_message(msg);    
  });
  // chat.onscroll = update_scroll();

  socket.on('message response', async function(msg){
    console.log(5);   
  })
};

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

function display_message(msg){
  console.log(msg)
  let p = document.createElement('P');
  p.innerHTML = msg;
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

