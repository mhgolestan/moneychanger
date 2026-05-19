from typing import Tuple, Dict
import os
import json
import requests
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import truststore

truststore.inject_into_ssl()
load_dotenv()

EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# Tool definition for function calling



def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    response = requests.get(
        f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    )
    if response.status_code == 200:
        data = response.json()
        conversion_result = round(data["conversion_result"], 2)
        return base, target, amount, conversion_result
    else:
        raise Exception(
            f"Error fetching exchange rate: {response.status_code} - {response.text}"
        )


def call_llm(textbox_input: str) -> Dict:
    """Make a call to gpt-4o-mini via GitHub Models with function calling enabled.
       The LLM decides whether to call get_exchange_rate based on the user's input."""
    # GitHub Models client using OpenAI-compatible endpoint
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=GITHUB_TOKEN,
    )

    MODEL = "gpt-4o-mini"
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


def run_pipeline(textbox_input: str) -> str:
    """Based on textbox_input, determine if tools are needed and return the result."""
    if not textbox_input.strip():
        return "Please enter an amount and currency to convert."
    try:
        completion = call_llm(textbox_input)
        message = completion.choices[0].message

        if message.tool_calls:  # LLM invoked get_exchange_rate
            tool_call = message.tool_calls[0]
            args = json.loads(tool_call.function.arguments)
            base = args["base"].upper()
            target = args["target"].upper()
            amount = args["amount"]
            base_out, target_out, amount_out, result = get_exchange_rate(base, target, amount)
            return f"{amount_out} {base_out} = **{result} {target_out}**"

        else:  # LLM responded directly without function calling
            return message.content or "Could not process the request."

    except Exception as e:
        return f"Error: {str(e)}"


# Gradio UI matching the provided layout
with gr.Blocks(
    title="Multilingual Money Changer",
    theme=gr.themes.Default(),
    css="""
        .main-col { max-width: 720px; margin: 2rem auto; padding: 1.5rem; }
        #title { font-size: 2rem; font-weight: 700; margin-bottom: 0.4rem; }
        #subtitle { color: #444; font-size: 0.92rem; margin-bottom: 1.2rem; }
    """,
) as demo:
    with gr.Column(elem_classes="main-col"):
        gr.Markdown("# Multilingual Money Changer", elem_id="title")
        gr.Markdown(
            "Enter the amount and currency. Non-english languages supported. "
            "(e.g., '100 USD to EUR' or '100 US money to England money'):",
            elem_id="subtitle",
        )
        textbox = gr.Textbox(label="", placeholder="", lines=1, show_label=False)
        submit_btn = gr.Button("Submit")
        output = gr.Markdown()

    submit_btn.click(fn=run_pipeline, inputs=textbox, outputs=output)
    textbox.submit(fn=run_pipeline, inputs=textbox, outputs=output)

if __name__ == "__main__":
    demo.launch()