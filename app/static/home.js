// selectors from the front end 
const chat = document.querySelector(".textarea");
const input = document.querySelector("input");
const form = document.getElementsByTagName("form")[0];
const logout = document.getElementsByTagName('a')[2];

// global variables
let user_messages = []; // messages sent by the current user 
var name = null // name of the user

window.onload = async function (){
  // on load we get all the previous messages sent in the chat room 
  new_messages = await load_messages();
  new_messages.forEach(msg => display_message(msg)); // for every message we display on the client's side 
}

  var socket = io.connect()
  socket.on('connect', async function(){
    name = await load_name();     // get the name from the flask session 
    socket.emit('event', {    // send the messages as json to the flask server 
      name: name, 
      message: "has entered the chat",
    })
    
    form.onsubmit = async function (e){
      e.preventDefault();       //prevents browser from reloading 
      var msg = input.value;
      if (msg === "")
        return false;
      input.value = "";
      user_messages.push(msg)     // push the messages sent by the client in his array 
      socket.emit('event',{
        name: name,
        message: msg,
      });
    }
  })

  socket.on('message response', async function(msg){    // receiving messages from server and displaying them 
    await display_message(msg);
  })

async function load_name(){       // async function for loading the name from the server session
    return  await fetch('/get_name')
    .then(async function (response) {
      return await response.json();
    }).then(function (text) {
        return text["name"]; 
    });
 }

async function load_messages(){       // async function for loading the messages from the server database
  return await fetch("/get_messages")
  .then(async function (response){
    return await response.json();
  })
  .then(function (text){
    return text["messages"];
  });
}

async function display_message(msg){ // displaying a message 

  let p1 = document.createElement('span')
  p1.innerText = msg["name"];
  p1.classList.add('name');

  let p2 = document.createElement('p')
  p2.innerText = msg["message"];
  
  let p3 = document.createElement('span');
  let new_time = format_time(msg["time"])
  p3.innerText = new_time;
  p3.classList.add("time");

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
  chat.scrollTop = chat.scrollHeight- chat.clientHeight; // makes the chat area autoscroll to the bottom on message received 
}

function format_time(time){ // utility function for changing the time format before displaying
  let yyyy = time.slice(0,4);
  let mm = time.slice(5,7);
  let dd = time.slice(8,10);
  let time_formatted = dd+ '-'+mm +'-'+ yyyy + ' '+ time.slice(11);
  return time_formatted;
}
