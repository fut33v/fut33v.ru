function reloadPage() {
    document.location.reload(true);
}
setTimeout(reloadPage, 60*1000);

function update() {
  let clock = document.getElementById('clock');
  let date = new Date(); // (*)
  let hours = date.getHours();
  if (hours < 10) hours = '0' + hours;
  clock.children[0].innerHTML = hours;

  let minutes = date.getMinutes();
  if (minutes < 10) minutes = '0' + minutes;
  clock.children[1].innerHTML = minutes;

  let dateElement = document.getElementById('date');
  let day = ('0' + date.getDate()).slice(-2);
  let month = ('0' +date.getMonth()).slice(-2);
  let year = 1900 + date.getYear();
  dateElement.children[0].innerHTML = day;
  dateElement.children[1].innerHTML = month;
  dateElement.children[2].innerHTML = year;
}
let timerId;
function clockStart() { // запустить часы
  timerId = setInterval(update, 1000);
  update(); // (*)
}

window.onload = function() {
    clockStart();
};

