import os
from dotenv import load_dotenv

# Detect environment mode from Docker Compose
MODE = os.getenv("MODE")  # Default to development if not set

# Define the path for each environment
ENV_PATHS = {
    "development": "leak_lock_ai/envs/development.env",
    "production": "leak_lock_ai/envs/production.env",
    "testing": "leak_lock_ai/envs/testing.env"
}

# Select the correct .env file
env_file = ENV_PATHS.get(MODE)

# Load environment variables
load_dotenv(env_file)

# Now environment variables can be accessed safely
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")

if not CHATGPT_API_KEY:
    raise ValueError(f"CHATGPT_API_KEY is missing in {env_file}. Check your .env file.")
