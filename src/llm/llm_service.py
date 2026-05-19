from typing import Dict
from openai import OpenAI
from langsmith import traceable
from src.core.config import GITHUB_TOKEN

MODEL = "gpt-4o-mini"


@traceable(name="call_llm", description="Call the LLM to process user input and determine if function calling is needed.")
def call_llm(textbox_input: str) -> Dict:
    """Make a call to gpt-4o-mini via GitHub Models with function calling enabled.
       The LLM decides whether to call get_exchange_rate based on the user's input."""
    # GitHub Models client using OpenAI-compatible endpoint
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=GITHUB_TOKEN,
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a multilingual currency conversion assistant. "
                "Extract the base currency, target currency, and amount from the user's input "
                "(which may be in any language) and call the get_exchange_rate function. "
                "Map country or descriptive names (e.g., 'US money', 'England money', 'Japanese yen') "
                "to the correct ISO 4217 currency code."
            ),
        },
        {"role": "user", "content": textbox_input},
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_exchange_rate",
                "description": "Get the exchange rate and convert an amount from one currency to another.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "base": {
                            "type": "string",
                            "description": "The ISO 4217 base currency code (e.g., USD, EUR, GBP)",
                        },
                        "target": {
                            "type": "string",
                            "description": "The ISO 4217 target currency code (e.g., USD, EUR, GBP)",
                        },
                        "amount": {
                            "type": "string",
                            "description": "The numeric amount to convert",
                        },
                    },
                    "required": ["base", "target", "amount"],
                },
            },
        }
    ]
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    return completion
