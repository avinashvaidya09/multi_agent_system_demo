"""This module acts as a facade layer for the agents.
"""

from cachetools import TTLCache
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from mas_autogen.app.agents.finance_group_chat_agent import FinanceGroupChatAgent
from mas_autogen.app.agents.weather_agent import WeatherAgent

router = APIRouter()


# cachetools for caching requests
session_cache = TTLCache(maxsize=100, ttl=3600)


def store_char_history(session_id: str, message: str):
    """TBD: Stores session chat history.

    Arguments:
        session_id -- Session id of the user.
        message -- user message.
    """
    if session_id in session_cache:
        session_cache[session_id].append(message)
    else:
        session_cache[session_id] = [message]


class ChatRequest(BaseModel):
    """Chat Request Base Model

    Arguments:
        BaseModel -- openai Base Model
    """

    agent_name: str
    message: str
    session_id: str


@router.post("/chat")
async def chat(request: ChatRequest):
    """API endpoint to interact with AI agents dynamically.

    Arguments:
        request -- Base Model.

    Returns:
        The agent response.
    """
    agent_name = request.agent_name
    if agent_name.lower() == "weather":
        agent_instance = WeatherAgent(agent_name=agent_name.lower())
    elif agent_name.lower() == "finance":
        agent_instance = FinanceGroupChatAgent(agent_name=agent_name.lower())
    else:
        raise HTTPException(
            status_code=404, detail=f"Agent '{agent_name}', not available at this point."
        )

    sender_agent, receiver_agent = agent_instance.create_ai_agents()

    response = agent_instance.start_chat(
        sender=sender_agent, receiver=receiver_agent, message=request.message
    )

    json_response = JSONResponse(content={"message": response})

    return json_response
