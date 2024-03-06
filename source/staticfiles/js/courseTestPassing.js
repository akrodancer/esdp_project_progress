let selectedAnswers = JSON.parse(localStorage.getItem('selectedAnswers')) || {};
let checkboxShapes = JSON.parse(localStorage.getItem('checkboxShapes')) || {};

let testContainer = document.getElementById('test-container');
let testId = testContainer.getAttribute('data-test-id');
let currentIndex = 0;
let testData = null;

fetch(`api/v1`)
    .then(response => response.json())
    .then(data => {
        testData = data;
        displayQuestion(currentIndex);
    });

function displayQuestion(index) {
    let question = testData.questions[index];
    testContainer.innerHTML = '';

    let questionElement = document.createElement('h2');
    questionElement.textContent = question.question_text;
    testContainer.appendChild(questionElement);

    let answersContainer = document.createElement('div');
    answersContainer.className = 'd-flex flex-row justify-content-between align-items-center flex-wrap';

    question.answers.forEach(answer => {
        let answerDiv = document.createElement('div');
        answerDiv.className = 'answer d-flex flex-column align-items-center mx-3';

        let checkboxDiv = document.createElement('div');
        checkboxDiv.className = 'custom-checkbox';

        let answerCheckbox = document.createElement('input');
        answerCheckbox.type = 'checkbox';
        answerCheckbox.id = 'answer-' + answer.id;
        answerCheckbox.value = answer.id;

        if (selectedAnswers.hasOwnProperty(question.id) && selectedAnswers[question.id].includes(answer.id)) {
            answerCheckbox.checked = true;
            checkboxDiv.style.backgroundColor = answerCheckbox.checked ? '#4484CF' : '#aaaaaa';
        }

        checkboxDiv.appendChild(answerCheckbox);
        checkboxDiv.style.borderRadius = checkboxShapes[answer.id] || "50%";

        checkboxDiv.addEventListener('click', function () {
            if (!answerCheckbox.checked) {
                answerCheckbox.checked = true;
                checkboxDiv.style.backgroundColor = answerCheckbox.checked ? '#4484CF' : '#aaaaaa';

                if (!selectedAnswers[question.id]) {
                    selectedAnswers[question.id] = [];
                }

                selectedAnswers[question.id].push(answer.id);

                if (selectedAnswers[question.id].length > 2) {
                    answerCheckbox.checked = false;
                    checkboxDiv.style.backgroundColor = answerCheckbox.checked ? '#4484CF' : '#aaaaaa';
                    selectedAnswers[question.id].pop();
                    return;
                }

                localStorage.setItem('selectedAnswers', JSON.stringify(selectedAnswers));

                if (selectedAnswers[question.id].length === 1) {
                    checkboxShapes[answer.id] = "50%";
                    localStorage.setItem('checkboxShapes', JSON.stringify(checkboxShapes));
                    checkboxDiv.style.borderRadius = "50%";
                } else {
                    checkboxShapes[answer.id] = "0";
                    localStorage.setItem('checkboxShapes', JSON.stringify(checkboxShapes));
                    checkboxDiv.style.borderRadius = "0";
                }
            }
        });

        let answerLabel = document.createElement('label');
        answerLabel.htmlFor = answerCheckbox.id;
        answerLabel.className = 'answertext mb-3';
        answerLabel.textContent = answer.answer_text;

        answerDiv.appendChild(answerLabel);
        answerDiv.appendChild(checkboxDiv);

        answersContainer.appendChild(answerDiv);
    });
    testContainer.appendChild(answersContainer);
}

document.getElementById('prevButton').onclick = function () {
    if (currentIndex > 0) {
        currentIndex--;
        displayQuestion(currentIndex);
    }
};

document.getElementById('nextButton').onclick = function () {
    if (currentIndex < testData.questions.length - 1) {
        currentIndex++;
        displayQuestion(currentIndex);
    }
};

document.getElementById('submitButton').onclick = function () {
    let filteredAnswers = {};

    for (let question in selectedAnswers) {
        if (selectedAnswers.hasOwnProperty(question)) {
            let lastAnswer = selectedAnswers[question][selectedAnswers[question].length - 1];
            filteredAnswers[question] = [lastAnswer];
        }
    }
    console.log(filteredAnswers);

    fetch('api/v1/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify(filteredAnswers)
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Response is not OK');
            }
        })
        .then(data => {
            console.log(data);
            localStorage.removeItem('selectedAnswers');
            localStorage.removeItem('checkboxShapes');
            window.location.href = `/online_tests/test/results/${data.user_test_id}/`;
        })
        .catch(error => console.error('Error:', error));
};