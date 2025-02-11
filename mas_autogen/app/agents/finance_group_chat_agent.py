"""This module is for finance agent.
"""

import autogen
from gen_ai_hub.proxy import GenAIHubProxyClient
from gen_ai_hub.proxy.native.openai import OpenAI as OpenAIProxy
from loguru import logger
from mas_autogen.app.agents.super_agent import SuperAgent
from mas_autogen.app.utils.aicoreclient import AICoreClient
from mas_autogen.app.utils.llm_config import (
    llm_config_for_finance_agent,
    llm_config_for_csr_agent,
    llm_config_for_group_chat_manager,
)
from mas_autogen.app.functions.finance_functions import (
    extract_customer_id_using_llm,
    get_customer_balance,
    get_customer_details,
    get_invoices,
)
from mas_autogen.app.utils.prompt_config import (
    FINANCE_AGENT_PROMPT,
    CSR_AGENT_PROMPT,
    GROUP_CHAT_MANAGER_PROMPT,
)


class FinanceGroupChatAgent(SuperAgent):
    """This class implements create_ai_agents method.

    Arguments:
        SuperAgent -- The agent framework parent class.
    """

    def create_ai_agents(self):

        gen_ai_hub_proxy_client = GenAIHubProxyClient()
        openai_proxy_client = OpenAIProxy(proxy_client=gen_ai_hub_proxy_client)

        csr_agent = autogen.AssistantAgent(
            name="csr_agent",
            system_message=CSR_AGENT_PROMPT,
            llm_config=llm_config_for_csr_agent,
        )

        finance_agent = autogen.AssistantAgent(
            name="finance_agent",
            system_message=FINANCE_AGENT_PROMPT,
            llm_config=llm_config_for_finance_agent,
        )

        user_proxy_agent = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            code_execution_config={
                "use_docker": False,
            },
            llm_config=False,
        )

        allowed_transitions = {
            user_proxy_agent: [finance_agent],
            finance_agent: [user_proxy_agent, csr_agent],
            csr_agent: [],
        }

        group_chat = autogen.GroupChat(
            agents=[user_proxy_agent, finance_agent, csr_agent],
            allowed_or_disallowed_speaker_transitions=allowed_transitions,
            speaker_transitions_type="allowed",
            messages=[],
            max_round=20,
            speaker_selection_method="auto",
        )

        groupchat_manager = autogen.GroupChatManager(
            name="chat_manager",
            groupchat=group_chat,
            max_consecutive_auto_reply=20,
            system_message=GROUP_CHAT_MANAGER_PROMPT,
            human_input_mode="NEVER",
            llm_config=llm_config_for_group_chat_manager,
            is_termination_msg=lambda x: isinstance(x, dict)
            and x.get("content")
            and "TERMINATE" in x["content"].strip(),
        )

        def send_text_message(phone_number: str, message: str) -> str:
            logger.info("******Text Message****** : " + phone_number)
            logger.info("###########################################")
            logger.info("Message: " + message)
            return "Message sent to the customer: " + message + " TERMINATE."

        def extract_customer_id(user_input: str) -> str:
            """
            Uses an LLM to extract a ZIP code from the user's input.

            Args:
            user_input (str): The user's query.

            Returns:
                str: The extracted ZIP code or None.
            """
            return extract_customer_id_using_llm(user_input=user_input)

        def fetch_customer_details(customer_id: str) -> dict:
            """Fetches the customer details.

            Arguments:
                customer_id -- The customer id

            Returns:
                The customer details.
            """
            return get_customer_details(customer_id)

        def fetch_customer_balance(customer_id: str) -> dict:
            """Fetches the customer balance.

            Arguments:
                customer_id -- The customer id.

            Returns:
                The customer balance.
            """
            return get_customer_balance(customer_id)

        def fetch_invoices(customer_id: str) -> dict:
            """Fetches the customer invoices.

            Arguments:
                customer_id -- The customer id.

            Returns:
                The customer invoices.
            """
            return get_invoices(customer_id)

        # Register functions with user proxy agent.
        user_proxy_agent.register_function(
            function_map={
                "extract_customer_id": extract_customer_id,
                "fetch_customer_details": fetch_customer_details,
                "fetch_customer_balance": fetch_customer_balance,
                "fetch_invoices": fetch_invoices,
                "send_text_message": send_text_message,
            }
        )

        csr_agent.register_model_client(model_client_cls=AICoreClient, client=openai_proxy_client)

        finance_agent.register_model_client(
            model_client_cls=AICoreClient, client=openai_proxy_client
        )

        groupchat_manager.register_model_client(
            model_client_cls=AICoreClient, client=openai_proxy_client
        )

        return user_proxy_agent, groupchat_manager
