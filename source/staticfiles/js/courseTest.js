document.addEventListener('DOMContentLoaded', function () {
    let testContainer = document.getElementById('test-container');
    let testId = testContainer.getAttribute('data-test-id');
    let currentIndex = 0;

    function showQuestion(index) {
        const questions = document.querySelectorAll('.question');
        questions.forEach((question, idx) => {
            if (idx === index) {
                question.style.display = 'block';
            } else {
                question.style.display = 'none';
            }
        });
        currentIndex = index;
        updateButtons();
    }

    function updateButtons() {
        const questions = document.querySelectorAll('.question');
        const prevButton = document.getElementById('prevButton');
        const nextButton = document.getElementById('nextButton');
        prevButton.disabled = currentIndex === 0;
        nextButton.disabled = currentIndex === questions.length - 1;
    }

    fetch(`/tests/test/${testId}/api/v1/`)
        .then(response => response.json())
        .then(test => {
            let questionsHtml = '';
            test.questions.forEach((question, index) => {
                let questionElement = `
                    <div class="question mt-5 mb-5" style="display: ${index === 0 ? 'block' : 'none'};">
                        <h3>${question.question_text}</h3>
                `;
                if (question.question_image) {
                    questionElement += `<img src="${question.question_image}" alt="Question Image">`;
                }
                questionElement += '<div class="checkboxes row mt-5 mb-5">';
                question.answers.forEach(answer => {
                    questionElement += `
                        <div class="col-3 mt-5 mb-5">
                            ${answer.answer_image ? `<img src="${answer.answer_image}" alt="Answer Image">` : `<label for="answer_${answer.id}">${answer.answer_text}</label><br>`}
                            <input type="checkbox" class="checkbox-style" name="question_${question.id}" id="answer_${answer.id}" value="${answer.id}">
                        </div>
                    `;
                });
                questionElement += '</div></div>';
                questionsHtml += questionElement;
            });
            testContainer.innerHTML = questionsHtml;
            updateButtons();
        });

    document.getElementById('prevButton').addEventListener('click', function() {
        if (currentIndex > 0) {
            showQuestion(currentIndex - 1);
        }
    });

    document.getElementById('nextButton').addEventListener('click', function() {
        const questions = document.querySelectorAll('.question');
        if (currentIndex < questions.length - 1) {
            showQuestion(currentIndex + 1);
        }
    });
});
