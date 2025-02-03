"""This module is agent framework parent class."""

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

    def start_chat(self, sender, receiver, message):
        """This function initiates the chat.

        Arguments:
            sender -- The sender agent.
            receiver -- The receiver agent.
            message -- The user message.

        Returns:
            The final answer or error.
        """
        response = sender.initiate_chat(
            receiver,
            message=message,
        )

        return response.chat_history[-1]["content"].replace("TERMINATE.", "").strip()
