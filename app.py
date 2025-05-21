import os
from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Use OPENAI_API_KEY from environment if available
openai.api_key = os.environ.get("OPENAI_API_KEY", "")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{'role': 'system', 'content': 'You are a friendly talking cat named Whiskers who loves chatting with children age 6-8.'},
                     {'role': 'user', 'content': user_message}],
            temperature=0.7,
            max_tokens=60,
        )
        assistant_reply = response.choices[0].message['content']
    except Exception as e:
        assistant_reply = "Sorry, I'm having trouble responding right now."
    return jsonify({'reply': assistant_reply})

if __name__ == '__main__':
    app.run(debug=True)
