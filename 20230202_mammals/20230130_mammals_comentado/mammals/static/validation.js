var form = document.getElementById("createForm");

const nick = document.getElementById("nick_input");
const firstName = document.getElementById("first_name_input");
const lastName = document.getElementById("last_name_input");
const phone = document.getElementById("phone_input");

var clearButton = document.getElementById("clearButton");
var hideButton = document.getElementById("hideButton");
var showButton = document.getElementById("showButton");

function onSubmitClicked(event) {
  // var nickInput = document.geteElementById("nick_input");
  // console.log("Here");
  if (nick.value.trim().length === 0) {
    nick.classList.add("error");
    alert("Nick required");
    return false;
  } else {
    nick.classList.remove("error");
  }

  if (firstName.value.trim().length === 0) {
    firstName.classList.add("error");
    alert("First Name required");
    return false;
  }

  if (lastName.value.trim().length === 0) {
    lastName.classList.add("error");
    alert("Last Name required");
    return false;
  }

  if (phone.value.trim().length === 0 || isNaN(phone.value)) {
    phone.classList.add("error");
    alert("Phone required");
    return false;
  }

  return true;
}

function clear() {
  nick.value = "";
  firstName.value = "";
  lastName.value = "";
  phone.value = "";
}

function hide() {
  form.style.display = "none";
}

function show() {
  form.style.display = "";
}

form.onsubmit = onSubmitClicked;

clearButton.onclick = clear;
hideButton.onclick = hide;
showButton.onclick = show;
