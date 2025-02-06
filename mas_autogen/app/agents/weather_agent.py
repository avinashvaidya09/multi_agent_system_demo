"""This module is for weather agent.
"""

import autogen
from mas_autogen.app.agents.super_agent import SuperAgent
from mas_autogen.app.utils.llm_config import llm_config_for_weather_agent
from mas_autogen.app.functions.weather_functions import get_weather_data, extract_zip_code_using_llm
from mas_autogen.app.utils.prompt_config import WEATHER_AGENT_PROMPT

class WeatherAgent(SuperAgent):
    """This class implements create_ai_agents method.

    Arguments:
        SuperAgent -- The agent framework parent class.
    """

    def create_ai_agents(self):

        weather_agent = autogen.AssistantAgent(
            name="weather_agent",
            system_message=WEATHER_AGENT_PROMPT,
            llm_config=llm_config_for_weather_agent,
        )

        user_proxy_agent = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",  # Ask user for missing information
            is_termination_msg=lambda x: isinstance(x, dict)
            and x.get("content")
            and "TERMINATE" in x["content"].strip(),
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

        # Register functions with user proxy agent.
        user_proxy_agent.register_function(
            function_map={
                "extract_zip_code": extract_zip_code,
                "fetch_weather_data": fetch_weather_data,
            }
        )

        return user_proxy_agent, weather_agent
