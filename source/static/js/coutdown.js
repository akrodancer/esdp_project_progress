let testEndContainer = document.getElementById('test-end-container');
let countdownElement = document.getElementById('countdown');
let countdownElementSecond = document.getElementById('countdown2');
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
    let hours = Math.floor(duration / 3600).toString().padStart(2, '0');
    let minutes = Math.floor((duration % 3600) / 60).toString().padStart(2, '0');
    let seconds = (duration % 60).toString().padStart(2, '0');
    let milliseconds = Math.floor((duration % 1) * 1000).toString().padStart(2, '0');
    countdownElement.textContent = countdownElementSecond.textContent = `${hours}:${minutes}:${seconds}:${milliseconds}`;
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


