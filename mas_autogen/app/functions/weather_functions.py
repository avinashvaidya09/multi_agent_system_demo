"""This module holds all the weather related functions.
"""

import requests

from langchain.schema import SystemMessage, HumanMessage
from loguru import logger
from mas_autogen.app.utils.ai_core_config import AICoreConfig
from mas_autogen.app.utils.config import WEATHER_API_URL, WEATHER_API_KEY

chat_llm = AICoreConfig().get_chat_llm()

def extract_zip_code_using_llm(user_input: str) -> str:
    """This function uses llms to extract zip code.

    Arguments:
        user_input -- The user input.

    Returns:
        The zip code.
    """

    input_messages = [
        SystemMessage(
            content="""
                    You are a helpful assistant extracting ZIP codes from user input. 
                    User input can be text like = 'Give me weather for 30041'
                    If the user input contains the zip code, extract it.
                    If the user input does not contain the zip code, 
                    use the last zip code mentioned in the session chat history provided along with the user input.
                    If no ZIP code is mentioned, return 'None'
                      """
        ),
        HumanMessage(
            content=f"User Input: '{user_input}' .If no ZIP code is present, then return 'None'."
        ),
    ]

    response = chat_llm.invoke(input=input_messages)

    zip_code = response.content.strip()
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
