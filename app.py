import os
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from config import OPENAI_API_KEY, DEBUG

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {'role': 'system', 'content': 'You are Hailey, an energetic sheep who loves to chat with children ages 6-7. Keep your replies short, fun, and easy to understand. Use simple words and short sentences. Be encouraging and positive. Share fun facts about sheep and farm life. Ask questions to keep the conversation going. Never use emojis or symbols in your responses.'},
                {'role': 'user', 'content': user_message}
            ],
            temperature=0.7,
            max_tokens=60,
        )
        assistant_reply = response.choices[0].message.content
    except Exception as e:
        print(f"Error: {str(e)}")  # Print error to console
        assistant_reply = f"Error: {str(e)}"
    return jsonify({'reply': assistant_reply})

@app.route('/tts', methods=['POST'])
def tts():
    """Convert text to speech using OpenAI's API and return an MP3."""
    text = request.json.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        audio_data = response.content
        return send_file(
            BytesIO(audio_data),
            mimetype='audio/mpeg'
        )
    except Exception as e:
        print(f"TTS Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=DEBUG)
