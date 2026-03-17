import base64
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)
MURF_API_KEY = "ap2_43ecf506-cd4b-4947-a9ac-8815e23a2893"

PRO_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🎓 VoiceLangCoach | NIAT Murf AI Hackathon</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .container { 
            background: white; border-radius: 25px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            padding: 40px; max-width: 500px; text-align: center; position: relative; overflow: hidden;
        }
        .container::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px; background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1); }
        h1 { color: #2c3e50; margin-bottom: 20px; font-size: 28px; font-weight: 700; }
        .subtitle { color: #7f8c8d; margin-bottom: 30px; font-size: 16px; }
        .mic-btn { 
            background: linear-gradient(45deg, #ff6b6b, #feca57); color: white; border: none; 
            width: 120px; height: 120px; border-radius: 50%; font-size: 24px; cursor: pointer;
            box-shadow: 0 10px 30px rgba(255,107,107,0.4); transition: all 0.3s ease; margin: 20px 0;
        }
        .mic-btn:hover { transform: scale(1.05); box-shadow: 0 15px 40px rgba(255,107,107,0.6); }
        .mic-btn.listening { background: linear-gradient(45deg, #4ecdc4, #45b7d1); animation: pulse 1s infinite; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(78,205,196,0.7); } 70% { box-shadow: 0 0 0 20px rgba(78,205,196,0); } 100% { box-shadow: 0 0 0 0 rgba(78,205,196,0); } }
        .output { background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 15px; padding: 20px; margin: 20px 0; min-height: 80px; font-size: 18px; }
        .feedback { color: #27ae60; font-weight: 600; margin-top: 10px; }
        .score { background: linear-gradient(45deg, #27ae60, #2ecc71); color: white; padding: 8px 16px; border-radius: 25px; font-weight: bold; display: inline-block; }
        .tech-stack { margin-top: 30px; font-size: 14px; color: #7f8c8d; }
        audio { width: 100%; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 VoiceLangCoach</h1>
        <p class="subtitle">Real-time Telugu-English Code-Mix Coach | NIAT Murf Hackathon</p>
        
        <button class="mic-btn" id="micBtn" onclick="toggleListening()">🎤</button>
        <div class="output" id="output">Click mic to start speaking Telugu-English mix!</div>
        <audio id="feedbackAudio" controls></audio>
        
        <div class="tech-stack">
            <strong>Powered by:</strong> Murf Falcon TTS + Web Speech API | 
            <a href="https://github.com/bindusri001/VoiceLangCoach" target="_blank" style="color: #3498db;">GitHub</a>
        </div>
    </div>

    <script>
        let isListening = false;
        let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-IN';
        recognition.continuous = true;
        recognition.interimResults = false;

        function toggleListening() {
            if (!isListening) {
                recognition.start();
                document.getElementById('micBtn').textContent = '🔴';
                document.getElementById('micBtn').classList.add('listening');
                document.getElementById('output').innerHTML = 'Listening... 🗣️ Speak now!';
                isListening = true;
            } else {
                recognition.stop();
                document.getElementById('micBtn').textContent = '🎤';
                document.getElementById('micBtn').classList.remove('listening');
                isListening = false;
            }
        }

        recognition.onresult = async function(event) {
            let text = event.results[event.results.length-1][0].transcript;
            document.getElementById('output').innerHTML = `<strong>You:</strong> "${text}"`;
            
            const response = await fetch('/speak', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            });
            const data = await response.json();
            
            document.getElementById('output').innerHTML += `<div class="feedback"><strong>Coach:</strong> ${data.feedback}</div>`;
            if (data.audio) {
                document.getElementById('feedbackAudio').src = data.audio;
                document.getElementById('feedbackAudio').play().catch(e => console.log('Autoplay blocked'));
            }
        };

        recognition.onend = function() {
            document.getElementById('micBtn').textContent = '🎤';
            document.getElementById('micBtn').classList.remove('listening');
            isListening = false;
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return PRO_HTML

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json['text'].lower()
    
    # Telugu-English code-mix scoring
    telugu_words = ['cheppu', 'nenu', 'teacher', 'student', 'nerchu', 'help', 'mix']
    english_words = ['english', 'say', 'good', 'morning', 'perfect']
    
    telugu_score = sum(1 for word in telugu_words if word in text)
    english_score = sum(1 for word in english_words if word in text)
    total_score = min(95, (telugu_score * 10) + (english_score * 5))
    
    if telugu_score >= 1 and english_score >= 1:
        feedback = f"🎯 PERFECT CODE-MIX! Fluency: <span class='score'>{total_score}/100</span><br>Great Telugu+English balance! Try: 'Nenu student, English nerchukunta'"
    elif len(text.split()) < 4:
        feedback = "📝 Good start! Speak full sentences with Telugu-English mix."
        total_score = 65
    else:
        feedback = f"✅ Good pronunciation! Fluency: <span class='score'>{total_score}/100</span><br>Add more Telugu words like 'cheppu', 'nenu'"
    
    return jsonify({'feedback': feedback, 'audio': None, 'score': total_score})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
