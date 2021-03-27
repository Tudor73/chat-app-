const button = document.querySelector(".send");
const chat = document.querySelector(".textarea");


button.addEventListener('click', addMessage);

function addMessage(event){
    let p = document.createElement('P');
    p.innerHTML = "hello";
    chat.append(p);
}
