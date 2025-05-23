# Kid Chat - Hailey the Energetic Sheep

A friendly chat application featuring Hailey, an energetic sheep who chats with children ages 6-7 using short, fun, and upbeat messages.

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
OPENAI_API_KEY=your_api_key_here
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
# Optional: configure persistent memory location and size
MEMORY_FILE=memory.json
MEMORY_LIMIT=20
```

## Running the Application

1. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Start the Flask server:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Features

- Chat with Hailey, an energetic sheep character
- Real-time responses using GPT-4
- Loading indicators
- Clear chat functionality
- Character limit on messages
- Enter key support for sending messages
- Persistent conversation memory with a configurable size limit

## Development

The application uses:
- Flask for the backend
- OpenAI API for chat responses
- Modern CSS for styling
- Vanilla JavaScript for interactivity

## Security

- API keys are stored in environment variables
- Input validation and sanitization
- Error handling for API failures
- Character limits on messages

## Testing

There is a minimal test checking that the home page loads successfully:

```bash
pytest
```

## Notes

The application attempts to use OpenAI's API. If no API key is provided or the request fails, Hailey will reply with a default error message.
