"""AI Core Config module
"""

from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client

from gen_ai_hub.proxy.langchain.openai import ChatOpenAI


class AICoreConfig:
    """Gen AI Core Config

    Arguments:
        OpenAIClient -- The Open AI Client
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def __init__(self):
        if not hasattr(self, "chat_llm"):
            self.chat_llm = None

    def _initialize(self):
        proxy_client = get_proxy_client("gen-ai-hub")
        self.chat_llm = ChatOpenAI(
            proxy_model_name="gpt-4o", proxy_client=proxy_client, temperature=0.7
        )

    def get_chat_llm(self):
        """Gets the ChatOpenAI client

        Returns:
            The ChatOpenAI.
        """
        return self.chat_llm
