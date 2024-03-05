let testEndContainer = document.getElementById('test-end-container');
let countdownElement = document.getElementById('countdown');
let duration = parseInt(testEndContainer.getAttribute('data-countdown'), 10);
let timer = setInterval(function () {
    duration--;
    let minutes = Math.floor(duration / 60);
    let seconds = duration % 60;
    countdownElement.textContent = minutes + ":" + (seconds  < 10 ? "0" : "") + seconds;
    if (duration <= 0) {
        document.getElementById('submitButton').click();
        clearInterval(timer);
    }
}, 1000);