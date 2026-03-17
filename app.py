from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head><title>🎓 VoiceLangCoach | NIAT Murf Hackathon</title>
<meta name="viewport" content="width=device-width">
<style>*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;align-items:center;justify-content:center;}
.container{background:white;border-radius:25px;box-shadow:0 25px 50px rgba(0,0,0,0.15);padding:40px;max-width:500px;text-align:center;}
h1{color:#2c3e50;font-size:28px;margin-bottom:10px;}
.subtitle{color:#7f8c8d;margin-bottom:30px;font-size:16px;}
.mic-btn{background:linear-gradient(45deg,#ff6b6b,#feca57);color:white;border:none;width:120px;height:120px;border-radius:50%;font-size:24px;cursor:pointer;box-shadow:0 15px 35px rgba(255,107,107,0.4);margin:20px 0;transition:all 0.3s;}
.mic-btn:hover{transform:scale(1.05);}
.mic-btn.listening{background:linear-gradient(45deg,#4ecdc4,#45b7d1);animation:pulse 1s infinite;}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(78,205,196,0.7);}70%{box-shadow:0 0 0 25px rgba(78,205,196,0);}100%{box-shadow:0 0 0 0 rgba(78,205,196,0);}}
.output{background:#f8f9fa;border:2px solid #e9ecef;border-radius:15px;padding:25px;margin:20px 0;font-size:18px;}
.you{color:#3498db;font-weight:600;}
.coach{color:#27ae60;font-weight:600;margin-top:15px;}
.score{background:linear-gradient(45deg,#27ae60,#2ecc71);color:white;padding:10px 20px;border-radius:25px;font-weight:bold;font-size:18px;display:inline-block;}
</style></head>
<body>
<div class="container">
<h1>🎓 VoiceLangCoach</h1>
<p class="subtitle">Real-time Telugu-English Code-Mix Coach<br>NIAT Murf AI Hackathon 2026</p>
<button class="mic-btn" id="micBtn" onclick="toggleMic()">🎤 Speak</button>
<div class="output" id="output">Click mic → Say "English lo cheppu nenu student"!</div>
</div>
<script>
let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
let synth = window.speechSynthesis;
let isListening = false;
recognition.lang = 'en-IN';
recognition.interimResults = false;

function toggleMic() {
    if(!isListening) {
        recognition.start();
        document.getElementById('micBtn').innerHTML = '🔴';
        document.getElementById('micBtn').classList.add('listening');
        document.getElementById('output').innerHTML = '🎤 Listening... Speak now!';
        isListening = true;
    } else {
        recognition.stop();
        document.getElementById('micBtn').innerHTML = '🎤';
        document.getElementById('micBtn').classList.remove('listening');
        isListening = false;
    }
}

recognition.onresult = function(e) {
    let text = e.results[0][0].transcript;
    let output = document.getElementById('output');
    output.innerHTML = `<div class="you">You: "${text}"</div>`;
    
    // Telugu-English scoring
    let telugu = text.toLowerCase().includes('cheppu') || text.toLowerCase().includes('nenu') || text.toLowerCase().includes('teacher');
    let english = text.toLowerCase().includes('english') || text.includes('good') || text.split(' ').length > 3;
    let score = telugu && english ? 95 : telugu ? 75 : english ? 65 : 45;
    
    let feedback = telugu && english ? 
        `🎯 PERFECT CODE-MIX! <div class="score">Score: ${score}/100</div>` :
        `✅ Good effort! <div class="score">Score: ${score}/100</div>`;
    
    output.innerHTML += `<div class="coach">${feedback}</div>`;
    
    // INSTANT SOUND FEEDBACK
    let utterance = new SpeechSynthesisUtterance(feedback.replace(/<[^>]*>/g, '') + ` Score ${score}`);
    utterance.lang = 'en-IN';
    utterance.rate = 0.9;
    synth.speak(utterance);
};

recognition.onend = function() {
    document.getElementById('micBtn').innerHTML = '🎤';
    document.getElementById('micBtn').classList.remove('listening');
    isListening = false;
};
</script>
</body></html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

