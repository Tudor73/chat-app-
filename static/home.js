const chat = document.querySelector(".textarea");
const input = document.querySelector("input");

$(function() {
    $('#sendBtn').on('click', function(e) {
    var msg = input.value;
    let p = document.createElement('P');
    p.innerHTML = input.value;
    chat.append(p);
    input.value = "";
    //   e.preventDefault()
      $.getJSON('/run',
        {message:msg},
          function(data) {
      });

      return false;
    });
  });
window.onload = function(){
  var loop = setInterval(update, 100);
  update();
}
function update(){

  fetch('/get_messages')
  .then(function (response) {
    return response.text();
  }).then(function (text) {
    console.log('GET response text:');
    console.log(text); // Print the greeting as text
  });
}





// button.addEventListener('click', addMessage);

// function addMessage(event){
//     event.preventDefault();

// }
