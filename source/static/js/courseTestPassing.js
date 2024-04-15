let testContainer = document.getElementById('question-container');
let checkboxesContainer = document.getElementById('chekboxes-container');
let nextButton = document.getElementById('nextButton');
let prevButton = document.getElementById('prevButton');
let currentIndex = 0;
let testData = null;
let selectedAnswers = JSON.parse(localStorage.getItem('selectedAnswers')) || {};
let checkboxShapes = JSON.parse(localStorage.getItem('checkboxShapes')) || {};

fetch(`api/v1`)
    .then(response => response.json())
    .then(data => {
        testData = data;
        displayQuestions(currentIndex);
        displayCheckboxes();
    });

function displayQuestions(startIndex) {
    testContainer.innerHTML = '';
    testContainer.classList.add('row');

    for (let i = startIndex; i < Math.min(startIndex + 4, testData.questions.length); i++) {
        let question = testData.questions[i];
        let questionElement = document.createElement('div');
        questionElement.classList.add('col-md-6');

        let questionContainer = document.createElement('div');
        questionContainer.classList.add('card', 'mb-3');

        let questionContent = document.createElement('div');
        questionContent.classList.add('card-body');

        let questionTitle = document.createElement('h5');
        questionTitle.classList.add('card-title');
        questionTitle.textContent = question.question_text;

        if (question.question_image) {
            let imageElement = document.createElement('img');
            imageElement.src = question.question_image;
            imageElement.classList.add('card-img-top');
            questionContent.appendChild(imageElement);
        } else {
            questionContent.appendChild(questionTitle);
        }

        let answersList = document.createElement('ul');
        answersList.classList.add('list-group', 'list-group-horizontal');
        question.answers.forEach(answer => {
            let answerItem = document.createElement('li');
            answerItem.classList.add('list-group-item', 'flex-fill', 'border-0');
            if (answer.answer_image) {
                let imageElement = document.createElement('img');
                imageElement.src = answer.answer_image;
                answerItem.appendChild(imageElement);
            } else {
                answerItem.textContent = answer.answer_text;
            }
            answersList.appendChild(answerItem);
        });

        questionContent.appendChild(answersList);
        questionContainer.appendChild(questionContent);
        questionElement.appendChild(questionContainer);
        testContainer.appendChild(questionElement);
    }
}

function displayCheckboxes() {
    const questions = testData.questions;
    const groupSize = 4;

    function createAnswersContainer(questionNumber) {
        const answersContainer = document.createElement('div');
        answersContainer.classList.add('d-flex', 'answers');

        const questionNumberSpan = document.createElement('h5');
        questionNumberSpan.classList.add('question-number')
        questionNumberSpan.textContent = `${questionNumber}.`;
        answersContainer.appendChild(questionNumberSpan);

        return answersContainer;
    }

    function createCheckbox(answer, questionId) {
        const checkboxContainer = document.createElement('div');
        checkboxContainer.classList.add('answer-container', 'custom-checkbox');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'answer';
        checkbox.value = answer.id;
        checkbox.dataset.questionId = questionId;

        if (selectedAnswers[questionId] && selectedAnswers[questionId].includes(answer.id)) {
            checkbox.checked = true;
            checkboxContainer.style.backgroundColor = '#044691';
            if (checkboxShapes[questionId] && checkboxShapes[questionId][answer.id]) {
                checkboxContainer.style.borderRadius = checkboxShapes[questionId][answer.id];
            }
        }

        checkboxContainer.addEventListener('click', function () {
            if (!checkbox.checked && (!selectedAnswers[questionId] || selectedAnswers[questionId].length < 2)) {
                checkbox.checked = true;
                checkboxContainer.style.backgroundColor = '#044691';

                if (!selectedAnswers[questionId]) {
                    selectedAnswers[questionId] = [];
                }

                selectedAnswers[questionId].push(answer.id);

                localStorage.setItem('selectedAnswers', JSON.stringify(selectedAnswers));

                if (selectedAnswers[questionId].length === 1) {
                    if (!checkboxShapes[questionId]) {
                        checkboxShapes[questionId] = {};
                    }
                    checkboxShapes[questionId][answer.id] = "100%";
                } else {
                    checkboxShapes[questionId][answer.id] = "0";
                }

                localStorage.setItem('checkboxShapes', JSON.stringify(checkboxShapes));
                checkboxContainer.style.borderRadius = checkboxShapes[questionId][answer.id];

                console.log(selectedAnswers);
            } else if (checkbox.checked) {
                const index = selectedAnswers[questionId].indexOf(answer.id);
                if (index > -1) {
                    selectedAnswers[questionId].splice(index, 1);
                    checkboxShapes[questionId][answer.id] = "0";
                    checkboxContainer.style.borderRadius = "0";
                }
                checkbox.checked = false;
                checkboxContainer.style.backgroundColor = '#D9D9D9';
                localStorage.setItem('selectedAnswers', JSON.stringify(selectedAnswers));
                localStorage.setItem('checkboxShapes', JSON.stringify(checkboxShapes));
            }
        });

        checkboxContainer.appendChild(checkbox);
        return checkboxContainer;
    }


    let groupContainer;
    let questionCounter = 1;

    questions.forEach((question, index) => {
        if (index % groupSize === 0) {
            groupContainer = document.createElement('div');
            groupContainer.classList.add('group-container');
            checkboxesContainer.appendChild(groupContainer);
        }
        const answersContainer = createAnswersContainer(questionCounter);
        question.answers.forEach(answer => {
            const checkbox = createCheckbox(answer, question.id);
            answersContainer.appendChild(checkbox);
        });
        groupContainer.appendChild(answersContainer);
        questionCounter++; // Увеличиваем счетчик вопросов
    });
}

nextButton.addEventListener('click', () => {
    const maxIndex = testData.questions.length - 4;
    if (currentIndex < maxIndex) {
        currentIndex += 4;
        displayQuestions(currentIndex);
    }
});

prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex -= 4;
        displayQuestions(currentIndex);
    }
});

document.getElementById('submitButton').onclick = function () {
    let filteredAnswers = {};
    for (let question in selectedAnswers) {
        if (selectedAnswers.hasOwnProperty(question)) {
            let lastAnswer = selectedAnswers[question][selectedAnswers[question].length - 1];
            filteredAnswers[question] = [lastAnswer];
        }
    }

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
        .catch(error => {
            console.error('Error:', error);
        });
};