// Parse the destinations data embedded in the page
const destinations = JSON.parse(document.getElementById('destinations-data').textContent);

// Game state variables
let currentQuestionIndex = 0;
let score = 0;
let correctCount = 0;
let wrongCount = 0;
let questions = [];

// Initialize the game: shuffle questions and start with the first one
function initGame() {
  questions = destinations.slice();
  shuffleArray(questions);
  currentQuestionIndex = 0;
  score = 0;
  correctCount = 0;
  wrongCount = 0;
  updateScore();
  loadQuestion();
}

// Fisher-Yates Shuffle to randomize an array
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// Load the current question
function loadQuestion() {
  document.getElementById('feedback').innerText = '';
  document.getElementById('nextBtn').disabled = true;
  
  const cluesDiv = document.getElementById('clues');
  const imageContainer = document.getElementById('image-container');
  const leftOptionsDiv = document.getElementById('left-options');
  const rightOptionsDiv = document.getElementById('right-options');
  
  cluesDiv.innerHTML = '';
  imageContainer.innerHTML = '';
  leftOptionsDiv.innerHTML = '';
  rightOptionsDiv.innerHTML = '';
  
  // Do not change body background image; always use initial background color
  document.body.style.backgroundImage = 'none';
  
  if (currentQuestionIndex >= questions.length) {
    cluesDiv.innerHTML = `<p>Game over! Your final score is ${score} (Correct: ${correctCount} | Wrong: ${wrongCount}).</p>`;
    document.getElementById('nextBtn').innerText = 'Play Again';
    document.getElementById('nextBtn').disabled = false;
    return;
  }
  
  const question = questions[currentQuestionIndex];
  
  // Display up to 2 clues
  const cluesToShow = question.clues.slice(0, 2);
  cluesToShow.forEach(clue => {
    const p = document.createElement('p');
    p.innerText = clue;
    cluesDiv.appendChild(p);
  });
  
  // Display the destination image if available in the image container
  if (question.image_url) {
    const img = document.createElement('img');
    img.src = question.image_url;
    img.alt = `Image of ${question.city}`;
    imageContainer.appendChild(img);
  }
  
  // Generate options: correct answer plus three random incorrect answers
  let options = [question.city];
  const otherCities = questions.filter(q => q.city !== question.city).map(q => q.city);
  shuffleArray(otherCities);
  options = options.concat(otherCities.slice(0, 3));
  shuffleArray(options);
  
  // Split options into two columns: left (first two) and right (last two)
  const leftOptions = options.slice(0, 2);
  const rightOptions = options.slice(2);
  
  leftOptions.forEach(option => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.innerText = option;
    btn.onclick = () => checkAnswer(btn, option, question.city, question.fun_fact);
    leftOptionsDiv.appendChild(btn);
  });
  
  rightOptions.forEach(option => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.innerText = option;
    btn.onclick = () => checkAnswer(btn, option, question.city, question.fun_fact);
    rightOptionsDiv.appendChild(btn);
  });
}

// Check the user's answer, reveal fun fact, and trigger animations
function checkAnswer(button, selected, correct, funFact) {
  const optionButtons = document.querySelectorAll('.option-btn');
  optionButtons.forEach(btn => btn.disabled = true);
  
  const feedbackDiv = document.getElementById('feedback');
  if (selected === correct) {
    button.classList.add('correct');
    feedbackDiv.innerHTML = `🎉 Correct! Fun Fact: ${funFact}`;
    score++;
    correctCount++;
    updateScore();
    // Trigger bursty confetti animation for correct answer
    confetti({ particleCount: 200, spread: 100, origin: { y: 0.6 } });
  } else {
    button.classList.add('wrong');
    feedbackDiv.innerHTML = `😢 Incorrect! Fun Fact: ${funFact}`;
    wrongCount++;
    updateScore();
    // Trigger full-screen cross animation for wrong answer
    triggerCrossAnimation();
    optionButtons.forEach(btn => {
      if (btn.innerText === correct) {
        btn.classList.add('correct');
      } else if (!btn.classList.contains('wrong')) {
        btn.classList.add('wrong');
      }
    });
  }
  document.getElementById('nextBtn').disabled = false;
}

// Trigger a full-screen cross animation (big red cross overlay) centered on screen
function triggerCrossAnimation() {
  const crossOverlay = document.getElementById('cross-overlay');
  crossOverlay.innerHTML = '<div class="cross-animation">❌</div>';
  crossOverlay.style.display = 'flex';
  setTimeout(() => {
    crossOverlay.style.display = 'none';
    crossOverlay.innerHTML = '';
  }, 2000);
}

// Load the next question or restart the game if finished
function nextQuestion() {
  if (currentQuestionIndex >= questions.length - 1) {
    initGame();
    document.getElementById('nextBtn').innerText = 'Next';
    return;
  }
  currentQuestionIndex++;
  loadQuestion();
}

// Update score display
function updateScore() {
  document.getElementById('scoreValue').innerText = score;
  document.getElementById('score-details').innerText = `Correct: ${correctCount} | Wrong: ${wrongCount}`;
}

// Challenge a Friend feature: open WhatsApp share popup with dynamic text only
document.getElementById('challengeBtn').addEventListener('click', () => {
  const username = document.getElementById('username').value.trim();
  if (!username) {
    alert('Please enter a unique username to challenge a friend.');
    return;
  }
  const shareMessage = encodeURIComponent(
    `Hey, I'm ${username} with a score of ${score} in Globetrotter Challenge! Can you beat me? Play now: ${window.location.href}`
  );
  const whatsappUrl = `https://api.whatsapp.com/send?text=${shareMessage}`;
  window.open(whatsappUrl, '_blank');
});

// Mode switching logic
const modeSwitch = document.getElementById('modeSwitch');
modeSwitch.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  document.body.classList.toggle('light-mode');
});

// Start the game when the page loads
window.onload = initGame;
