"""This module holds all finance related functions.
"""

import json
import os
from loguru import logger
from langchain.schema import SystemMessage, HumanMessage
from mas_autogen.app.utils.ai_core_config import AICoreConfig

BASE_DIRECTORY = os.path.join(os.path.dirname(__file__), "../data")
chat_llm = AICoreConfig().get_chat_llm()

def load_data_from_json(file_name: str) -> dict:
    """This function loads data from the json.

    Arguments:
        file_name -- The file name.

    Returns:
        The data in JSON format.
    """
    file_path = os.path.join(BASE_DIRECTORY, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    logger.info(data)
    return data


def get_customer_balance(customer_id: str) -> dict:
    """This function gets the balance for the customer id.

    Arguments:
        customer_id -- The customer id.

    Returns:
        The customer balance in JSON format.
    """
    balances = load_data_from_json("balances.json")
    for balance in balances["balances"]:
        if balance["customer_id"] == customer_id:
            return balance

    return {"error": f"No balance found for customer '{customer_id}'"}


def get_customer_contact(customer_id: str) -> dict:
    """Get customer contact information.

    Arguments:
        customer_id -- The customer id.

    Returns:
        The customer information.
    """
    customer_info = load_data_from_json("customer.json")
    for customer in customer_info["customers"]:
        if customer["customer_id"] == customer_id:
            return customer

    return {"error": f"No details found for customer '{customer_id}'"}


def get_customer_details(customer_id: str) -> dict:
    """This function gets the customer details for the customer id.

    Arguments:
        customer_id -- The customer id.

    Returns:
        The customer details in JSON format.
    """
    customer_details = load_data_from_json("customer_details.json")
    for customer_detail in customer_details["customer_details"]:
        if customer_detail["customer_id"] == customer_id:
            return customer_detail

    return {"error": f"No details found for customer '{customer_id}'"}


def get_invoices(customer_id: str) -> dict:
    """This function gets the invoices for the customer id.

    Arguments:
        customer_id -- The customer id.

    Returns:
        The invoices details in JSON format.
    """
    invoices = load_data_from_json("invoices.json")
    for invoice in invoices["invoices"]:
        if invoice["customer_id"] == customer_id:
            return invoice

    return {"error": f"No invoice found for customer '{customer_id}'"}


def extract_customer_id_using_llm(user_input: str) -> str:
    """This function uses llms to extract customer id.

    Arguments:
        user_input -- The user input.

    Returns:
        The customer id.
    """
    input_messages = [
        SystemMessage(
            content="""
                        You are a helpful assistant extracting customer id from user input.
                        User input can be text like = 'Give me balance for CUST002' or 'Give me invoices for CUST001'
                        If the user input does not contain the customer id, 
                        use the last customer id mentioned in the Session Chat History provided along with the user input.
                        You do not have to keep on looping through all the customers in the Session Chat History. 
                        Just the get the last customer id mentioned in the Session Chat History.
                        If you do not find customer id in the user input then return 'None'
                        """
        ),
        HumanMessage(
            content=f" User input '{user_input}'.If no customer id is present, then return 'None'."
        ),
    ]
    response = chat_llm.invoke(input=input_messages)
    customer_id = response.content.strip()
    return customer_id
