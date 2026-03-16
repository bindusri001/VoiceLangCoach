from flask import Flask, render_template, request, jsonify
import requests
import json
import base64
import openai
from datetime import datetime

app = Flask(__name__)

# YOUR KEYS (REPLACE WITH REAL ONES)
MURF_API_KEY = "ap2_43ecf506-cd4b-4947-a9ac-8815e23a2893"  # YOUR KEY ✅
OPENAI_API_KEY = "sk-proj-xxx..."  # Free Grok/Claude key OR skip for now

# Murf Falcon TTS Call
def text_to_speech(text, voice_id="en-US-AnaNeural"): 
    url = "https://api.murf.ai/v1/falcon/tts"
    headers = {
        "Authorization": f"Bearer {MURF_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_id": voice_id,  # Telugu/English voices
        "speed": 1.0
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        audio_b64 = response.json()["audio"]
        return base64.b64decode(audio_b64)
    return None

# LLM Feedback (Grammar/Pronunciation correction)
def get_feedback(user_text):
    # Mock LLM - Replace with real OpenAI/Grok later
    errors = []
    if "cheppu" in user_text.lower() and "english" not in user_text.lower():
        errors.append("Use 'English lo cheppu' for code-mixing practice")
    if len(user_text.split()) < 3:
        errors.append("Speak complete sentences (5+ words)")
    
    feedback = "Great effort! " + "; ".join(errors) if errors else "Perfect pronunciation! Ready for next quiz."
    return feedback

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    user_text = request.json['text']
    feedback = get_feedback(user_text)
    
    # Generate TTS audio
    audio = text_to_speech(feedback)
    if audio:
        audio_b64 = base64.b64encode(audio).decode()
        return jsonify({'feedback': feedback, 'audio': f'data:audio/wav;base64,{audio_b64}'})
    return jsonify({'error': 'TTS failed'})

if __name__ == '__main__':
    app.run(debug=True)
