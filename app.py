import os
from flask import Flask, render_template, request, jsonify
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
                {'role': 'system', 'content': 'You are Whiskers, a playful talking cat who loves to chat with kids ages 6-8. Keep your replies short, fun, and upbeat!'},
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

if __name__ == '__main__':
    app.run(debug=DEBUG)
