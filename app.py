import os
import json
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from config import OPENAI_API_KEY, DEBUG, MEMORY_FILE, MEMORY_LIMIT

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Persistent memory helpers
def load_memory():
    """Load conversation history from disk."""
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_memory(memory):
    """Persist conversation history to disk, trimming to MEMORY_LIMIT."""
    trimmed = memory[-MEMORY_LIMIT:]
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(trimmed, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    try:
        memory = load_memory()
        messages = [
            {
                'role': 'system',
                'content': 'You are Leila, an energetic sheep who loves to chat with children ages 6-7. Keep your replies short, fun, and easy to understand. Use simple words and short sentences. Be encouraging and positive. Ask questions to keep the conversation going. Never use emojis or symbols in your responses.'
            }
        ] + memory + [{'role': 'user', 'content': user_message}]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=60,
        )
        assistant_reply = response.choices[0].message.content

        memory.append({'role': 'user', 'content': user_message})
        memory.append({'role': 'assistant', 'content': assistant_reply})
        save_memory(memory)
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
