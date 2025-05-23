import os
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from config import OPENAI_API_KEY, DEBUG

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

HISTORY_LIMIT = 20

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    history = request.json.get('history', [])
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    messages = [
        {
            'role': 'system',
            'content': (
                'You are Leila, an energetic sheep who loves to chat with '
                'children ages 6-7. Keep your replies short, fun, and easy '
                'to understand. Use simple words and short sentences. Be '
                'encouraging and positive. Ask questions to keep the '
                'conversation going. Never use emojis or symbols in your '
                'responses. Remember you are chatting with Katherine, who '
                'is 6 years old and loves sheep, drawing, and playing '
                'outside.'
            )
        }
    ]

    if isinstance(history, list):
        for msg in history[-HISTORY_LIMIT:]:
            role = 'user' if msg.get('isUser') else 'assistant'
            text = msg.get('text', '')
            messages.append({'role': role, 'content': text})

    messages.append({'role': 'user', 'content': user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
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


@app.route('/correct', methods=['POST'])
def correct():
    """Use GPT to auto-correct transcribed speech text."""
    text = request.json.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'You are a helpful assistant that fixes mistakes in '
                        'short phrases transcribed from speech recognition. '
                        'Return only the corrected text.'
                    )
                },
                {'role': 'user', 'content': text}
            ],
            temperature=0,
            max_tokens=60,
        )
        corrected = response.choices[0].message.content.strip()
        return jsonify({'corrected': corrected})
    except Exception as e:
        print(f"Correction Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=DEBUG)
