    // DATA SOAL - Edit bagian ini untuk mengganti pertanyaan
    const questions = [{
            question: "She _____ to school every day.",
            options: ["go", "goes", "going", "gone"],
            correct: 1
        },
        {
            question: "I _____ watching TV when you called me yesterday.",
            options: ["am", "was", "were", "is"],
            correct: 1
        },
        {
            question: "They have _____ finished their homework.",
            options: ["yet", "already", "still", "never"],
            correct: 1
        },
        {
            question: "Which sentence is correct?",
            options: [
                "He don't like coffee",
                "He doesn't likes coffee",
                "He doesn't like coffee",
                "He not like coffee"
            ],
            correct: 2
        },
        {
            question: "The book _____ by millions of people around the world.",
            options: ["reads", "is read", "are read", "reading"],
            correct: 1
        }
    ];

    let currentQuestion = 0;
    let correctAnswers = 0;
    let wrongAnswers = 0;
    let selectedAnswer = null;

    const questionText = document.getElementById('question-text');
    const questionNumber = document.getElementById('question-number');
    const optionsContainer = document.getElementById('options-container');
    const feedback = document.getElementById('feedback');
    const btnSubmit = document.getElementById('btn-submit');
    const btnNext = document.getElementById('btn-next');
    const btnRestart = document.getElementById('btn-restart');
    const currentQuestionSpan = document.getElementById('current-question');
    const totalQuestionsSpan = document.getElementById('total-questions');
    const correctCountSpan = document.getElementById('correct-count');
    const wrongCountSpan = document.getElementById('wrong-count');
    const quizContainer = document.getElementById('quiz-container');
    const resultBox = document.getElementById('result-box');

    function loadQuestion() {
        const q = questions[currentQuestion];
        questionNumber.textContent = `Pertanyaan ${currentQuestion + 1}`;
        questionText.textContent = q.question;
        currentQuestionSpan.textContent = currentQuestion + 1;
        totalQuestionsSpan.textContent = questions.length;

        optionsContainer.innerHTML = '';
        selectedAnswer = null;
        feedback.style.display = 'none';
        feedback.className = 'feedback';
        btnSubmit.style.display = 'block';
        btnNext.style.display = 'none';

        q.options.forEach((option, index) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option';
            optionDiv.textContent = `${String.fromCharCode(65 + index)}. ${option}`;
            optionDiv.onclick = () => selectOption(index);
            optionsContainer.appendChild(optionDiv);
        });
    }

    function selectOption(index) {
        if (selectedAnswer !== null) return;

        const options = document.querySelectorAll('.option');
        options.forEach(opt => opt.classList.remove('selected'));
        options[index].classList.add('selected');
        selectedAnswer = index;
    }

    function checkAnswer() {
        if (selectedAnswer === null) {
            alert('Pilih jawaban terlebih dahulu!');
            return;
        }

        const q = questions[currentQuestion];
        const options = document.querySelectorAll('.option');

        options.forEach(opt => opt.classList.add('disabled'));

        if (selectedAnswer === q.correct) {
            options[selectedAnswer].classList.add('correct');
            feedback.className = 'feedback correct';
            feedback.textContent = '✓ Benar! Jawaban Anda tepat.';
            correctAnswers++;
        } else {
            options[selectedAnswer].classList.add('wrong');
            options[q.correct].classList.add('correct');
            feedback.className = 'feedback wrong';
            feedback.textContent =
                `✗ Salah! Jawaban yang benar adalah: ${String.fromCharCode(65 + q.correct)}. ${q.options[q.correct]}`;
            wrongAnswers++;
        }

        correctCountSpan.textContent = correctAnswers;
        wrongCountSpan.textContent = wrongAnswers;
        btnSubmit.style.display = 'none';
        btnNext.style.display = 'block';
    }

    function nextQuestion() {
        currentQuestion++;
        if (currentQuestion < questions.length) {
            loadQuestion();
        } else {
            showResult();
        }
    }

    function showResult() {
        quizContainer.style.display = 'none';
        resultBox.style.display = 'block';

        const score = (correctAnswers / questions.length) * 100;
        document.getElementById('final-score').textContent = `${correctAnswers}/${questions.length}`;

        let message = '';
        if (score === 100) {
            message = '🌟 Sempurna! Anda menguasai materi ini!';
        } else if (score >= 80) {
            message = '👍 Bagus sekali! Tingkatkan terus!';
        } else if (score >= 60) {
            message = '👌 Cukup baik! Masih ada ruang untuk berkembang.';
        } else {
            message = '💪 Jangan menyerah! Terus berlatih ya!';
        }

        document.getElementById('result-message').textContent = message;
    }

    function restart() {
        currentQuestion = 0;
        correctAnswers = 0;
        wrongAnswers = 0;
        correctCountSpan.textContent = 0;
        wrongCountSpan.textContent = 0;
        quizContainer.style.display = 'block';
        resultBox.style.display = 'none';
        loadQuestion();
    }

    btnSubmit.onclick = checkAnswer;
    btnNext.onclick = nextQuestion;
    btnRestart.onclick = restart;

    // Mulai quiz
    loadQuestion();