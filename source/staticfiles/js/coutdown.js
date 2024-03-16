let testEndContainer = document.getElementById('test-end-container');
let countdownElement = document.getElementById('countdown');
let initialTime = localStorage.getItem('initialTime');

if (initialTime) {
    let elapsedTime = Math.floor((new Date().getTime() - parseInt(initialTime, 10)) / 1000); // Прошедшее время с начала теста в секундах
    let remainingTime = parseInt(testEndContainer.getAttribute('data-countdown'), 10) - elapsedTime;
    duration = remainingTime > 0 ? remainingTime : 0;
} else {
    duration = parseInt(testEndContainer.getAttribute('data-countdown'), 10);
    localStorage.setItem('initialTime', new Date().getTime().toString());
}

let timer = setInterval(function () {
    duration--;
    let minutes = Math.floor(duration / 60);
    let seconds = duration % 60;
    countdownElement.textContent = minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
    document.getElementById('submitButton').addEventListener('click', function () {
        clearInterval(timer);
        localStorage.removeItem('initialTime');
    });
    if (duration <= 0) {
        document.getElementById('submitButton').click();
        clearInterval(timer);
        localStorage.removeItem('initialTime');
    }
}, 1000);


