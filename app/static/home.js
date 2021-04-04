const chat = document.querySelector(".textarea");
const input = document.querySelector("input");
const form = document.getElementsByTagName("form")[0];
const logout = document.getElementsByTagName('a')[2];

let user_messages = [];
const ADDRESS = "http://127.0.0.1/5000";


window.onload = async function (){
  new_messages = await load_messages();
  new_messages.forEach(msg => display_message(msg));
}


  var socket = io.connect()
  var name = null 
  socket.on('connect', async function(){
    name = await load_name();
    socket.emit('event', {
      name: name, 
      message: "has entered the chat",
    })
    
    form.onsubmit = async function (e){
      e.preventDefault();
      var msg = input.value;
      if (msg === "")
        return false;
      input.value = "";
      user_messages.push(msg)
      socket.emit('event',{
        name: name,
        message: msg,
      });
    }
  })

  socket.on('message response', async function(msg){
    await display_message(msg);
  })

  // logout.onclick = function() {
  //   socket.emit('event',{
  //     name: name,
  //     message: " has left the chat ",
  //   });
  //   // socket.disconnect();
  // }

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

  let p1 = document.createElement('span')
  p1.innerText = msg["name"];
  p1.classList.add('name');

  let p2 = document.createElement('p')
  p2.innerText = msg["message"];
  
  let p3 = document.createElement('span');
  p3.innerText = msg["time"];
  p3.classList.add("time")

  console.log(msg["message"])
  if (msg["message"].includes('entered')){
    p2.style.color = "green";
  }
  if (msg["message"].includes('left')){
    p2.style.color = "red";
  }
  let div = document.createElement('div');
  div.appendChild(p1);
  div.appendChild(p3);
  div.appendChild(p2);

  div.classList.add("chat-bubble");
  if(user_messages.includes(msg["message"])){
    div.classList.add("darker");
  }
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight- chat.clientHeight;
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

