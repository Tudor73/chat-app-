const chat = document.querySelector(".textarea");
const input = document.querySelector("input");

$(function() {
    $('#sendBtn').on('click', function(e) {
    var msg = input.value;
    let p = document.createElement('P');
    p.innerHTML = input.value;
    chat.append(p);
    input.value = "";
    console.log(msg);
    //   e.preventDefault()
      $.getJSON('/run',
        {message:msg},
          function(data) {
    
      });
      return false;
    });
  });






// button.addEventListener('click', addMessage);

// function addMessage(event){
//     event.preventDefault();

// }
