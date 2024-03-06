let testEndContainer = document.getElementById('test-end-container');
let countdownElement = document.getElementById('countdown');
let initialTime = localStorage.getItem('initialTime');
let currentTime = new Date().getTime();

if(initialTime) {
    let elapsedTime = Math.floor((currentTime - initialTime) / 1000); // Convert ms to s
    let remainingTime = parseInt(testEndContainer.getAttribute('data-countdown'), 10) - elapsedTime;
    duration = remainingTime > 0 ? remainingTime : 0;
} else {
    duration = parseInt(testEndContainer.getAttribute('data-countdown'), 10);
    localStorage.setItem('initialTime', currentTime.toString());
}

let timer = setInterval(function () {
    duration--;
    let minutes = Math.floor(duration / 60);
    let seconds = duration % 60;
    countdownElement.textContent = minutes + ":" + (seconds  < 10 ? "0" : "") + seconds;
    if (duration <= 0) {
        document.getElementById('submitButton').click();
        clearInterval(timer);
        localStorage.removeItem('initialTime');
    }
}, 1000);