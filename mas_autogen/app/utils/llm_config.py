"""Hold the llm config for the agents
"""

from mas_autogen.app.utils.config import OPENAI_API_KEY

llm_config_for_weather_agent = {
    "model": "gpt-4",
    "api_key": OPENAI_API_KEY,
    "functions": [
        {
            "name": "extract_zip_code",
            "description": "Extract the ZIP code from the given text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "User-provided text from which to extract the ZIP code.",
                    }
                },
                "required": ["user_input"],
            },
        },
        {
            "name": "fetch_weather_data",
            "description": "Fetch the current weather for a given ZIP code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_code": {
                        "type": "string",
                        "description": "The 5-digit ZIP code for which to retrieve weather.",
                    }
                },
                "required": ["zip_code"],
            },
        },
    ],
    "timeout": 120,
}

llm_config_for_finance_agent = {
    "model": "gpt-4",
    "api_key": OPENAI_API_KEY,
    "functions": [
        {
            "name": "extract_customer_id",
            "description": "Extract the customer id from the given text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "User-provided text from which to extract the customer id.",
                    }
                },
                "required": ["user_input"],
            },
        },
        {
            "name": "fetch_customer_details",
            "description": "Fetch customer details with the given customer id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer id to retrieve details",
                    }
                },
                "required": ["customer_id"],
            },
        },
        {
            "name": "fetch_customer_balance",
            "description": "Fetch customer balance with the given customer id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer id to retrieve customer balance",
                    }
                },
                "required": ["customer_id"],
            },
        },
        {
            "name": "fetch_invoices",
            "description": "Fetch customer invoices with the given customer id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer id to retrieve customer invoices",
                    }
                },
                "required": ["customer_id"],
            },
        },
        {
            "name": "fetch_disputed_items",
            "description": "Fetch customer disputed items with the given customer id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer id to retrieve customer disputed items",
                    }
                },
                "required": ["customer_id"],
            },
        },
    ],
    "timeout": 120,
}
