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
    feedback = f"Great pronunciation! '{text}' → Try more Telugu mix like 'Nenu student English nerchukunta'. NIAT Murf Hackathon entry!"
    # Mock audio for demo (real Murf needs voice_id fix)
    audio_b64 = "UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQ=="
    return jsonify({'feedback': feedback, 'audio': f'data:audio/wav;base64,{audio_b64}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
