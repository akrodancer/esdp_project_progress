const progressBar = document.querySelector('.progress-bar-inner');
const progress = parseInt(progressBar.getAttribute('data-progress'));

function updateProgressBar() {
    progressBar.style.width = progress + '%';
}
updateProgressBar();

let dataContainer = document.getElementById('data-container');
let correctAnswerCount = parseInt(dataContainer.getAttribute('data-correct-answer-count'));
let incorrectAnswerCount = parseInt(dataContainer.getAttribute('data-incorrect-answer-count'));
let totalQuestionsCount = parseInt(dataContainer.getAttribute('data-total-questions-count'));
let correctPercent = (correctAnswerCount / totalQuestionsCount) * 100;
let incorrectPercent = (incorrectAnswerCount / totalQuestionsCount) * 100;
let correctPercentElement = document.getElementById('correctPercent');
let incorrectPercentElement = document.getElementById('incorrectPercent');
correctPercentElement.textContent = correctPercent.toFixed();
incorrectPercentElement.textContent = incorrectPercent.toFixed();