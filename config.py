import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY is not set in environment variables")

# Flask Configuration
DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "dev")

# Persistent memory configuration
MEMORY_FILE = os.getenv("MEMORY_FILE", "memory.json")
MEMORY_LIMIT = int(os.getenv("MEMORY_LIMIT", "20"))
