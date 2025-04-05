function runCommand() {
    const input = document.getElementById('terminal').value.trim();
    const feedback = document.getElementById('feedback');
  
    if (input === 'docker version') {
      feedback.textContent = '✅ Correct! Your shipping yard is ready for action!';
      feedback.style.color = '#00ff7f';
    } else {
      feedback.textContent = '❌ Incorrect command. Try again!';
      feedback.style.color = '#ff5555';
    }
  }
  