var soundElements = document.querySelectorAll('.sound-item');
var audioElements = {};

// Initialize audio elements
soundElements.forEach(function(soundElement) {
  var soundId = soundElement.querySelector('audio').id;
  var audio = new Audio(soundElement.querySelector('audio').src);
  audioElements[soundId] = audio;
});

soundElements.forEach(function(soundElement) {
  var playButton = soundElement.querySelector('.play-button');
  var audio = audioElements[playButton.getAttribute('data-sound')];
  var progressBar = soundElement.querySelector('.progress');

  playButton.addEventListener('click', function() {
    if (audio.paused) {
      audio.play();
      playButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-stop-circle-fill" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM6.5 5A1.5 1.5 0 0 0 5 6.5v3A1.5 1.5 0 0 0 6.5 11h3A1.5 1.5 0 0 0 11 9.5v-3A1.5 1.5 0 0 0 9.5 5h-3z"/></svg>'
      progressBar.style.display = 'block';
      updateProgressBar(audio, progressBar);
    } else {
      audio.pause();
      playButton.innerHTML =  '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16"><path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/></svg>';
      progressBar.style.display = 'none';
    }
  });

  audio.addEventListener('timeupdate', function() {
    updateProgressBar(audio, progressBar);
  });

  audio.addEventListener('ended', function() {
    playButton.innerHTML =  '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16"><path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/></svg>';
    progressBar.style.display = 'none';
  });
});

function updateProgressBar(audio, progressBar) {
  var currentTime = audio.currentTime;
  var duration = audio.duration;
  var progress = (currentTime / duration) * 100;
  progressBar.querySelector('.progress-bar').style.width = progress + '%';
  progressBar.querySelector('.progress-bar').textContent = Math.floor(progress) + '%';
}
