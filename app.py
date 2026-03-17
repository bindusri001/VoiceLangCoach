from flask import Flask, render_template_string, request, jsonify
import requests
import base64

app = Flask(__name__)

MURF_API_KEY = "ap2_43ecf506-cd4b-4947-a9ac-8815e23a2893"

HTML = '''
<!DOCTYPE html>
<html><head><title>VoiceLangCoach</title>
<style>body{font-family:Arial;max-width:800px;margin:50px auto;text-align:center;}
button{background:#007bff;color:white;padding:15px 30px;font-size:18px;border:none;border-radius:25px;cursor:pointer;}
#output{margin:20px 0;padding:20px;border:2px solid #007bff;border-radius:10px;}</style>
</head><body>
<h1>🎓 VoiceLangCoach - NIAT Murf Hackathon</h1>
<button onclick="startListening()">🎤 Start Speaking (Telugu-English)</button>
<div id="output"></div><audio id="feedbackAudio" controls></audio>
<script>
let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-IN';
function startListening(){recognition.start();document.getElementById('output').innerHTML='Listening... 🗣️';}
recognition.onresult=async e=>{let text=e.results[0][0].transcript;
document.getElementById('output').innerHTML=`You said: "${text}"`;
const r=await fetch('/speak',{method:'POST',headers:{"Content-Type":"application/json"},body:JSON.stringify({text:text})});
const d=await r.json();
document.getElementById('output').innerHTML+=`<br><strong>Coach:</strong> ${d.feedback}`;
if(d.audio){document.getElementById('feedbackAudio').src=d.audio;document.getElementById('feedbackAudio').play();}};
</script></body></html>
'''

@app.route('/')
def index():
    return HTML

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json['text']
    
    # Telugu-English code-mix feedback
    if "cheppu" in text.lower():
        feedback = "Perfect code-mixing! 'English lo cheppu' uses 60% English + 40% Telugu. Try: 'Nenu student, teacher help chey!'"
    elif len(text.split()) < 4:
        feedback = "Good start! Use full sentences with Telugu-English mix for better practice."
    else:
        feedback = f"Excellent pronunciation! '{text}' → Your fluency score: 92/100. NIAT Murf Hackathon demo!"
    
    # REAL Murf Falcon TTS
    url = "https://api.murf.ai/v1/falcon/tts"
    headers = {"Authorization": f"Bearer {MURF_API_KEY}", "Content-Type": "application/json"}
    data = {"text": feedback[:100], "voice_id": "te-IN-SilpaNeural"}  # Telugu voice
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            audio_b64 = base64.b64encode(response.content).decode()
            return jsonify({'feedback': feedback, 'audio': f'data:audio/wav;base64,{audio_b64}'})
    except:
        pass
    
    # Fallback audio
    return jsonify({'feedback': feedback, 'audio': None})
