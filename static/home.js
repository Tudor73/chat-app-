const chat = document.querySelector(".textarea");
const input = document.querySelector("input");
const form = document.getElementsByTagName("form")[0];


const ADDRESS = "http://127.0.0.1/5000";



window.onload = function(){
  var socket = io.connect()

  socket.on('connect', async function(){
    var name = await load_name();
    var msg = name + " has entered the chat ";
    socket.send(msg);

    new_messages = await load_messages();
    new_messages.forEach(msg => display_message(msg));
  })


  form.onsubmit = async function (e){
    e.preventDefault();
    var msg = input.value;
    input.value = "";

    let user_name = await load_name();
    var message_to_show = user_name+": "+ msg;
    display_message(message_to_show);
    socket.send(message_to_show);
  }
  
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
  chat.appendChild(p);
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

