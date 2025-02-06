"""This module is agent parent class."""

from abc import ABC, abstractmethod


class SuperAgent(ABC):
    """Agent Framework class.

    Arguments:
        ABC -- The Abstract Base Class.
    """

    def __init__(self, agent_name: str = None):
        self.agent_name = agent_name

    @abstractmethod
    def create_ai_agents(self):
        """This is an abstract method."""

    def start_chat(self, sender, receiver, message, session_history):
        """This function initiates the chat.

        Arguments:
            sender -- The sender agent.
            receiver -- The receiver agent.
            message -- The user message.

        Returns:
            The final answer or error.
        """
        session_history_for_user = (
            "Session Chat History: " + ":".join(f"{msg}." for msg in session_history)
            if session_history
            else ""
        )
        response = sender.initiate_chat(
            receiver,
            message=(f"{message}{"."} {session_history_for_user}"),
        )

        return response.chat_history[-1]["content"].replace("TERMINATE.", "").strip()
