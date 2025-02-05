"""This module is for weather agent.
"""

import autogen
from mas_autogen.app.agents.super_agent import SuperAgent
from mas_autogen.app.utils.llm_config import llm_config_for_finance_agent
from mas_autogen.app.functions.finance_functions import (
    extract_customer_id_using_llm,
    get_customer_balance,
    get_customer_details,
    get_disputed_items,
    get_invoices,
)

class FinanceAgent(SuperAgent):
    """This class implements create_ai_agents method.

    Arguments:
        SuperAgent -- The agent framework parent class.
    """

    def create_ai_agents(self):

        finance_agent = autogen.AssistantAgent(
            name="finance_agent",
            system_message=(
                """
                You are a financial assistant. Your job is to extract the customer id 
                from the user's input. You are responsible for: 
                a. Get customer details
                b. Get customer balances
                c. Get customer invoices
                d. Get customer disputed items

                You understand what the user wants from the user input.
                Examples:
                1. "Get me the customer details for customer 1234" - You will call 
                    get_customer_details and return response. You will not get any more details if not asked.
                
                2. "Get me the balance for the customer 1234" - 
                    - You will first call get_customer_details, check if customer is active.
                    - If customer is active, you will proceed to get the customer balance 
                    using get_customer_balance function.
                
                3. For invoices and disputed items, you will follow similar approach as mentioned 
                   in point 2 but use get_invoices and get_disputed_items functions respctively.

                If there are multiple items, provide it in a list with numbers.
                
                You will provide suggestions to the user about the next possible steps.

                If the user says, "Thanks" or "Done" or "Bye", respond professionally.

                Once the data is retrieved and If current task is complete, 
                you will return the response and reply 'TERMINATE.'.

                You must explicitly state 'TERMINATE.' at the end of your response. 
                
                """
            ),
            llm_config=llm_config_for_finance_agent,
        )

        user_proxy_agent = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",  # Ask user for missing information
            is_termination_msg=lambda x: isinstance(x, dict)
            and x.get("content")
            and "TERMINATE" in x["content"].strip(),
            code_execution_config={
                "use_docker": False,
            },
        )

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

        def fetch_disputed_items(customer_id: str) -> dict:
            """Fetches the customer disputed items.

            Arguments:
                customer_id -- The customer id.

            Returns:
                The disputed items.
            """
            return get_disputed_items(customer_id)

        # Register functions with user proxy agent.
        user_proxy_agent.register_function(
            function_map={
                "extract_customer_id": extract_customer_id,
                "fetch_customer_details": fetch_customer_details,
                "fetch_customer_balance": fetch_customer_balance,
                "fetch_invoices": fetch_invoices,
                "fetch_disputed_items": fetch_disputed_items,
            }
        )

        return user_proxy_agent, finance_agent
