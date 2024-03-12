let testContainer = document.getElementById('question-container');
let checkboxesContainer = document.getElementById('chekboxes-container');
let nextButton = document.getElementById('nextButton');
let prevButton = document.getElementById('prevButton');
let currentIndex = 0;
let testData = null;
let selectedAnswers = {};

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

        checkboxContainer.addEventListener('click', function () {
            if (!checkbox.checked) {
                checkbox.checked = true;
                checkboxContainer.style.backgroundColor = checkbox.checked ? '#4484CF' : '#aaaaaa';

                if (!selectedAnswers[questionId]) {
                    selectedAnswers[questionId] = [];
                }

                if (selectedAnswers[questionId].length === 1) {
                    checkboxContainer.style.borderRadius = "0";
                }

                selectedAnswers[questionId].push(answer.id);
                if (selectedAnswers[questionId].length > 2) {
                    checkbox.checked = false;
                    checkboxContainer.style.backgroundColor = checkbox.checked ? '#4484CF' : '#aaaaaa';
                    selectedAnswers[questionId].pop();
                }
                console.log(selectedAnswers);
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
            window.location.href = `/online_tests/test/results/${data.user_test_id}/`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
};
