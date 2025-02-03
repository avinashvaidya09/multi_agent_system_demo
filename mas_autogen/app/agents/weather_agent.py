"""_summary_
Returns:
    _description_
"""

import autogen
from mas_autogen.app.utils.config import OPENAI_API_KEY
from mas_autogen.app.functions.weather_functions import get_weather_data, extract_zip_code_using_llm

llm_config = {
    "model": "gpt-4",
    "api_key": OPENAI_API_KEY,
    "functions": [
        {
            "name": "extract_zip_code",
            "description": "Extract the ZIP code from the given text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "User-provided text from which to extract the ZIP code.",
                    }
                },
                "required": ["user_input"],
            },
        },
        {
            "name": "fetch_weather_data",
            "description": "Fetch the current weather for a given ZIP code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_code": {
                        "type": "string",
                        "description": "The 5-digit ZIP code for which to retrieve weather.",
                    }
                },
                "required": ["zip_code"],
            },
        },
    ],
    "timeout": 120,
}

weather_agent = autogen.AssistantAgent(
    name="weather_agent",
    system_message=(
        "You are a weather assistant. Your job is to extract the ZIP code from the user's input. "
        " and call weather data retreival. Once the weather data is retrieved, return the response and reply 'TERMINATE'."
        " You must explicitly state 'TERMINATE' at the end of your response. "
    ),
    llm_config=llm_config,
)


user_proxy_agent = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # Enables the LLM to ask the user for missing information
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "use_docker": False,
    },
)




def extract_zip_code(user_input: str) -> str:
    """
    Uses an LLM to extract a ZIP code from the user's input.

    Args:
        user_input (str): The user's query.

    Returns:
        str: The extracted ZIP code or None.
    """
    return extract_zip_code_using_llm(user_input=user_input)


def fetch_weather_data(zip_code: str) -> dict:
    """
    Calls weather API to get the weather details using zip code.

    Args:
        zip_code (str): zip code

    Returns:
        dict: Weather details or an error message.
    """
    return get_weather_data(zip_code)


# Register tools as functions
user_proxy_agent.register_function(
    function_map={"extract_zip_code": extract_zip_code, "fetch_weather_data": fetch_weather_data}
)


def get_weather_forcast(user_input: str) -> dict:
    """_summary_

    Arguments:
        user_input -- _description_

    Returns:
        _description_
    """
    response = user_proxy_agent.initiate_chat(
        weather_agent,
        message=f"Given user input: '{user_input}', extract the ZIP code using `extract_zip_code`,"
        " then fetch weather data using `fetch_weather_data`.",
    )

    return response.chat_history[-1]["content"].replace("TERMINATE", "").strip()
