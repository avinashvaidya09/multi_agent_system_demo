"""
config.py

This module loads the environment variables.
"""

import os
from dotenv import load_dotenv


def load_environment_variables():
    """Loads env variables from .env file"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, "..", ".env")
    load_dotenv(env_path)


# Load .env at import time if not already loaded
if not os.getenv("OPENAI_API_KEY"):
    load_environment_variables()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# API URLS
WEATHER_API_URL = os.getenv("WEATHER_API_URL")
