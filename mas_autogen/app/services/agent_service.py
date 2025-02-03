"""_summary_
Returns:
    _description_
"""

from fastapi import APIRouter, HTTPException
from mas_autogen.app.agents.weather_agent import WeatherAgent

router = APIRouter()


@router.get("/chat")
async def chat(agent_name: str, message: str):
    """API endpoint to interact with AI agents dynamically.

    Arguments:
        agent_name -- The name of the agent.
        message -- The user input message.

    Returns:
        The agent response.
    """

    if agent_name.lower() == "weather_agent":
        agent_instance = WeatherAgent(agent_name=agent_name.lower())
    else:
        raise HTTPException(
            status_code=404, detail=f"Agent with '{agent_name}' not available at this point."
        )

    sender_agent, receiver_agent = agent_instance.create_ai_agents()

    response = agent_instance.start_chat(
        sender=sender_agent, receiver=receiver_agent, message=message
    )

    return response
