"""_summary_"""

from abc import ABC, abstractmethod


class AgentFramework(ABC):
    """_summary_

    Arguments:
        ABC -- _description_
    """

    def __init__(self, agent_name: str = None):
        self.agent_name = agent_name

    @abstractmethod
    def create_ai_agents(self):
        """_summary_

        Arguments:
            message -- _description_
        """
        pass

    def start_chat(self, sender, receiver, message):
        """_summary_

        Arguments:
            sender -- _description_
            receiver -- _description_
            message -- _description_

        Returns:
            _description_
        """
        response = sender.initiate_chat(
            receiver,
            message=message,
        )

        return response.chat_history[-1]["content"].replace("TERMINATE.", "").strip()
