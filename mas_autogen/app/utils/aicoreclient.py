"""Gen AI Core Proxy Client
"""

from typing import Any, Dict
from openai import OpenAI
from openai.types.chat import ChatCompletion
from autogen.oai.client import OpenAIClient
from gen_ai_hub.proxy import GenAIHubProxyClient
from gen_ai_hub.proxy.native.openai import OpenAI as OpenAIProxy


class AICoreClient(OpenAIClient):
    """Gen AI Hub Core Client

    Arguments:
        OpenAIClient -- Extends OpenAIClient
    """

    def __init__(self, kwargs, client: OpenAI | None = None):

        if client is None:
            client = OpenAIProxy(proxy_client=GenAIHubProxyClient())

        super().__init__(client)

    def create(self, params: Dict[str, Any]) -> ChatCompletion:

        params.pop("model_client_cls", None)
        return super().create(params)
