const chat = document.querySelector(".textarea");
const input = document.querySelector("input");

const ADDRESS = "http://127.0.0.1/5000"


window.onload = function(){
  var socket = io.connect()

  socket.on('connect', async function(){
    var name = await load_name();
    console.log(name);
    socket.send("Connected ");
  })
  socket.on('message', function(msg){
    msg = input.value;
    // console.log(msg);
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




// $(function() {
//   $('#sendBtn').on('click', function(e) {
//   var msg = input.value;
//   let p = document.createElement('P');
//   p.innerHTML = input.value;
//   chat.append(p);
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

