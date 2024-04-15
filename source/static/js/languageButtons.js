function filterTests(language) {
    localStorage.setItem('activeLanguage', language);
    window.location.href = `/online_tests/all_tests/?language=${language}`;
}

document.addEventListener('DOMContentLoaded', function() {
    const activeLanguage = localStorage.getItem('activeLanguage');
    if (activeLanguage) {
        const activeButton = document.querySelector(`.button[data-language="${activeLanguage}"]`);
        if (activeButton) {
            activeButton.classList.add('active');
        }
    }
    else {
        const activeButton = document.querySelector(`.button[data-language=""]`);
        if (activeButton) {
            activeButton.classList.add('active');
        }
    }
});