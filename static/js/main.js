document.addEventListener('DOMContentLoaded', () => {
  let historyData = [];
  let cameraOn = false;
  let lastGesture = "";
  let voiceEnabled = false;
  let meaningEnabled = false;
  let handLinesEnabled = true;
  const toggleBtn = document.getElementById('toggleCamera');
  const img = document.getElementById('cameraFeed');
  const voiceBtn = document.getElementById('toggleVoiceBtn');
  const meaningBtn = document.getElementById('toggleMeaningBtn');
  const handLinesBtn = document.getElementById('toggleLandmarksBtn');
  // ✅ Get the new meaning display element
  const gestureMeaningElement = document.getElementById('gestureMeaning'); 

  // 🔹 Initial button states
  voiceBtn.textContent = "Voice: ON";
  meaningBtn.textContent = "Meaning: ON";
  meaningBtn.style.display = 'none'; // hidden until voice ON
  handLinesBtn.textContent = handLinesEnabled ? "Hide Hand Lines" : "Show Hand Lines";
  
  const gestureMeanings = {
// ... (gestureMeanings object remains the same) ...
    "Hi/Hello/Bye 👋": "Greeting gesture",
    "Fist 👊": "Strong or Stop gesture",
    "Call Me 📞": "Phone call gesture",
    "I Love You ❤️": "Gesture expressing love",
    "Rock On 🤘": "Gesture for rock music or excitement",
    "Peace ✌️": "Victory or calm gesture",
    "Point Up ☝️": "Indicates pointing upwards",
    "OK 👌": "Gesture meaning everything is fine",
    "Unknown 🤷‍♂️": "Gesture not recognized"
  };

  // 🔹 Voice toggle (remains the same)
  voiceBtn.addEventListener('click', () => {
    voiceEnabled = !voiceEnabled;
    voiceBtn.textContent = voiceEnabled ? "Voice: OFF" : "Voice: ON";
    // Show/hide meaning button based on voice status
    meaningBtn.style.display = voiceEnabled ? 'inline-block' : 'none';
  });
  
  // 🔹 Meaning toggle
  meaningBtn.addEventListener('click', () => {
    meaningEnabled = !meaningEnabled;
    meaningBtn.textContent = meaningEnabled ? "Meaning: OFF" : "Meaning: ON";
    // ✅ Hide the visual meaning immediately when toggled OFF
    if (!meaningEnabled && gestureMeaningElement) {
        gestureMeaningElement.style.display = 'none';
        gestureMeaningElement.textContent = '';
    }
  });

// ... (toggleCamera and speakText functions remain the same) ...
  
  // 🔹 Hand lines toggle (remains the same)
  handLinesBtn.addEventListener('click', async () => {
    const res = await fetch('/toggle_landmarks', { method: 'POST' });
    const data = await res.json();
    handLinesEnabled = data.show_landmarks;
    handLinesBtn.textContent = handLinesEnabled ? "Hide Hand Lines" : "Show Hand Lines";
  });
  
  // 🔹 Camera toggle
  async function toggleCamera() {
    if (!cameraOn) {
      await fetch('/start_camera', { method: 'POST' });
      img.src = '/video_feed';
      toggleBtn.textContent = 'Stop Camera';
      cameraOn = true;
    } else {
      await fetch('/stop_camera', { method: 'POST' });
      img.src = '';
      toggleBtn.textContent = 'Start Camera';
      cameraOn = false;
    }
  }
  if (toggleBtn) toggleBtn.addEventListener('click', toggleCamera);
  
  // 🔹 Speech synthesis
  function speakText(text) {
    const synth = window.speechSynthesis;
    synth.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 1.1;
    utter.pitch = 1;
    synth.speak(utter);
  }
  
  // 🔹 Update gesture, history, and voice
  async function updateGesture() {
    try {
      const res = await fetch('/gesture');
      const data = await res.json();
      const label = data.label || 'No Hands Detected';
      const hand = data.handedness || 'Unknown';

      document.getElementById('gestureLabel').textContent = label;
      document.getElementById('handLabel').textContent = `Hand: ${hand}`;
      
      // ✅ Logic to display the gesture meaning
      const meaning = gestureMeanings[label] || "Meaning not available";
      
      if (meaningEnabled && label !== "No Hands Detected") {
        gestureMeaningElement.textContent = `----> : ${meaning}....`;
        gestureMeaningElement.style.display = 'block';
      } else {
        gestureMeaningElement.style.display = 'none';
        gestureMeaningElement.textContent = '';
      }
      
      const timestamp = new Date().toLocaleTimeString();
      const newEntry = `${timestamp} — ${label} (${hand})`;

      if (historyData[0] !== newEntry) {
        historyData.unshift(newEntry);
        if (historyData.length > 10) historyData.pop();
      }

      const historyContainer = document.getElementById('gestureHistory');
      if (historyContainer) {
        historyContainer.innerHTML = historyData.map(e => `<div class="history-entry">${e}</div>`).join('');
      }

      // 🔹 Speak gesture & meaning if enabled
      if (label !== lastGesture && label !== "No Hands Detected") {
        if (voiceEnabled) speakText(label);
        if (voiceEnabled && meaningEnabled) {
          // The meaning text for speech is already calculated
          speakText(meaning);
        }
        lastGesture = label;
      }
    } catch (err) {
      console.error("Error fetching gesture:", err);
    }
    requestAnimationFrame(updateGesture);
  }
  
  // Check the initial landmark status (good practice for refresh)
  fetch('/get_landmark_status')
    .then(res => res.json())
    .then(data => {
        handLinesEnabled = data.show_landmarks;
        handLinesBtn.textContent = handLinesEnabled ? "Hide Hand Lines" : "Show Hand Lines";
    });

  updateGesture();
});