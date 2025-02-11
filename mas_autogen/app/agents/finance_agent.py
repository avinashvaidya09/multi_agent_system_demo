"""This module is for finance agent.
"""

import autogen
from mas_autogen.app.agents.super_agent import SuperAgent
from mas_autogen.app.utils.llm_config import llm_config_for_finance_agent
from mas_autogen.app.functions.finance_functions import (
    extract_customer_id_using_llm,
    get_customer_balance,
    get_customer_details,
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
                b. get customer contact information
                c. Get customer balances
                d. Get customer invoices

                You understand what the user wants from the user input.
                Examples:
                1. "Get me the customer details for customer 1234" - You will call 
                    fetch_customer_details and return response. You will not get any more details if not asked.
                
                2. If the user asks for email id or phone number for contacting the customer,
                   For example - "I think I want to contact the customer CUST002" or "Give me email id to contact this customer"
                   then you will call fetch_customer_details and return response to the user. You will give this information even if the 
                   customer is inactive.
                
                3. "Get me the balance for the customer 1234" - 
                    - You will first call get_customer_details, check if customer is active.
                    - If customer is active, you will proceed to get the customer balance 
                    using fetch_customer_balance function.
                
                4. For invoices, you will follow similar approach as mentioned 
                   in point 3 but use fetch_invoices function respctively.

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
            human_input_mode="NEVER",
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

        # Register functions with user proxy agent.
        user_proxy_agent.register_function(
            function_map={
                "extract_customer_id": extract_customer_id,
                "fetch_customer_details": fetch_customer_details,
                "fetch_customer_balance": fetch_customer_balance,
                "fetch_invoices": fetch_invoices,
            }
        )

        return user_proxy_agent, finance_agent
