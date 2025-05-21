# Kid Chat

This is a simple Flask web application that provides a colorful chat interface for kids (ages 6-8) to talk with a friendly cat named **Whiskers**.

## Features

- Friendly cat emoji as the chat companion
- "Speak" button to send a message
- "Stop" button (currently does nothing but can be extended)
- Colorful, kid-friendly UI
- Uses OpenAI's API to generate responses (requires `OPENAI_API_KEY` environment variable)

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python app.py
```

3. Open your browser at `http://localhost:5000` to chat with Whiskers.

## Testing

There is a minimal test checking that the home page loads successfully:

```bash
pytest
```

## Notes

The application attempts to use OpenAI's API. If no API key is provided or the request fails, Whiskers will reply with a default error message.
