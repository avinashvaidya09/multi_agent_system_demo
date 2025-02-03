"""This module holds all the weather related functions.
"""

import requests
import openai
from loguru import logger
from mas_autogen.app.utils.config import WEATHER_API_URL, WEATHER_API_KEY, OPENAI_API_KEY


def extract_zip_code_using_llm(user_input: str) -> str:
    """This function uses llms to extract zip code.

    Arguments:
        user_input -- The user input.

    Returns:
        The zip code.
    """
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant extracting ZIP codes from user input. "
                "User input can be text like = 'Give me weather for 30041'"
                "You only accept 5 digit USA zip codes. "
                "If the user input is not a valid 5 digit USA zip code "
                "then return 'None'",
            },
            {
                "role": "user",
                "content": f"'{user_input}'."
                "If no ZIP code is present, then return 'None'.",
            },
        ],
    )

    zip_code = response.choices[0].message.content.strip()
    return zip_code


def get_weather_data(zip_code: str) -> dict:
    """This function calls weather api to get the data.

    Arguments:
        zip_code -- The zip code.

    Returns:
        The location, temperature and condition.
    """
    if not WEATHER_API_KEY:
        logger.error("Weather API key is missing")
        return {"error": "Weather API key is not configured"}

    parameters = {"key": WEATHER_API_KEY, "q": zip_code}

    try:
        response = requests.get(WEATHER_API_URL, params=parameters, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "location": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return {"error": "Failed to fetch weather data."}
