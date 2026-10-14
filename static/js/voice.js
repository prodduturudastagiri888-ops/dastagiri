// Smart Krishi Voice Interface (Web Speech API - Speech Recognition & Synthesis)

class KrishiVoice {
  constructor() {
    this.recognition = null;
    this.synth = window.speechSynthesis || null;
    this.isListening = false;
    this.initSpeechRecognition();
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;

      this.recognition.onstart = () => {
        this.isListening = true;
        this.updateVoiceStatus("Listening... / వింటున్నాను...", true);
      };

      this.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        this.handleTranscript(transcript);
      };

      this.recognition.onerror = (event) => {
        console.warn("Speech recognition error:", event.error);
        this.updateVoiceStatus("Voice input error", false);
        this.isListening = false;
      };

      this.recognition.onend = () => {
        this.isListening = false;
        this.updateVoiceStatus("", false);
      };
    } else {
      console.log("Web Speech API not supported in this browser.");
    }
  }

  startListening(targetInputId = "chatInput") {
    if (!this.recognition) {
      alert("Voice input is not supported in this browser. Please use Chrome, Edge, or a modern browser.");
      return;
    }
    this.activeTargetId = targetInputId;
    const currentLang = localStorage.getItem("smart_krishi_lang") || "te";
    this.recognition.lang = currentLang === "te" ? "te-IN" : "en-IN";
    try {
      this.recognition.start();
    } catch (e) {
      this.recognition.stop();
    }
  }

  handleTranscript(text) {
    const target = document.getElementById(this.activeTargetId || "chatInput");
    if (target) {
      target.value = text;
      // Trigger input event
      target.dispatchEvent(new Event("input"));
      // If it's the chatbot input and has form, auto-focus
      target.focus();
    }
  }

  speak(text) {
    if (!this.synth) return;
    this.stopSpeaking();
    
    // Strip markdown formatting for cleaner speech
    const cleanText = text.replace(/[*_#`[\]()]/g, " ").replace(/\s+/g, " ").trim();
    const utterance = new SpeechSynthesisUtterance(cleanText);
    const currentLang = localStorage.getItem("smart_krishi_lang") || "en";
    
    utterance.lang = currentLang === "te" ? "te-IN" : "en-IN";
    utterance.rate = 0.95; // Slightly slower for clarity in rural settings
    utterance.pitch = 1.0;

    this.synth.speak(utterance);
  }

  stopSpeaking() {
    if (this.synth && this.synth.speaking) {
      this.synth.cancel();
    }
  }

  updateVoiceStatus(msg, active) {
    const badge = document.getElementById("voiceStatusBadge");
    if (badge) {
      if (active) {
        badge.style.display = "inline-flex";
        badge.innerHTML = `<span class="spinner-grow spinner-grow-sm me-1"></span> ${msg}`;
      } else {
        badge.style.display = "none";
      }
    }
  }
}

window.krishiVoice = new KrishiVoice();
