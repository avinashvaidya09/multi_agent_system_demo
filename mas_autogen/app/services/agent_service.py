"""_summary_
Returns:
    _description_
"""

from typing import Dict, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mas_autogen.app.agents.finance_agent import FinanceAgent
from mas_autogen.app.agents.weather_agent import WeatherAgent

router = APIRouter()

# temporary session chat history. Can be replaced by redis
session_chat_history_messages: Dict[str, List[str]] = {}


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
        agent_instance = FinanceAgent(agent_name=agent_name.lower())
    else:
        raise HTTPException(
            status_code=404, detail=f"Agent '{agent_name}' not available at this point."
        )

    sender_agent, receiver_agent = agent_instance.create_ai_agents()

    response = agent_instance.start_chat(
        sender=sender_agent,
        receiver=receiver_agent,
        message=request.message,
        session_history=session_chat_history_messages.get(request.session_id),
    )

    if request.session_id not in session_chat_history_messages:
        session_chat_history_messages[request.session_id] = [request.message]

    else:
        session_chat_history_messages[request.session_id].append(request.message)

    return response
