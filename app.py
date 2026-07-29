import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app) # Gives your phone permission to connect securely

# Links your brain to your free Google AI Studio token wrapper
client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://googleapis.com"
)

@app.route('/webhook', methods=['POST'])
def handle_phone_command():
    data = request.json or {}
    user_command = data.get("command", "")
    
    if not user_command:
        return jsonify({"reply": "I am listening, but no command was received."}), 400

    # The Core Auto-Correction & Bilingual Translation Prompt
    system_instruction = (
        "You are Jarvis, an elite personal assistant. The user will talk in English, Nepali, "
        "or mixed 'Nepglish'. Automatically clear any audio stutters, spelling errors, or "
        "mispronunciations silently. Figure out their true intent and execute accurately."
    )
    
    # Process the command using your free un-capped Gemini processing engine
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_command}
        ]
    )
    
    jarvis_reply = response.choices.message.content
    return jsonify({"reply": jarvis_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
