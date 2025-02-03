"""_summary_
Returns:
    _description_
"""
from fastapi import APIRouter
from mas_autogen.app.agents.weather_agent import get_weather_forcast

router = APIRouter()


@router.get("/weather")
async def fetch_weather(query: str):
    """
    API endpoint to fetch weather based on user input.

    Args:
        query (str): The user's query (e.g., "Give me weather for 30041").

    Returns:
        dict: Weather details or an error message.
    """
    return get_weather_forcast(query)
