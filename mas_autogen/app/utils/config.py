"""
This module loads the environment variables.
"""

import os
from dotenv import load_dotenv


def load_environment_variables():
    """Loads enviroment variables from .env"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, "..", ".env")
    if env_path is not None:
        load_dotenv(env_path)
    else:
        load_dotenv()


# Load .env at import time if not already loaded
if not os.getenv("OPENAI_API_KEY"):
    load_environment_variables()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# API URLS
WEATHER_API_URL = os.getenv("WEATHER_API_URL")
