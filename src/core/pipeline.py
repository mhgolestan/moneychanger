import json
from langsmith import traceable
from src.llm.llm_service import call_llm
from src.core.tools import get_exchange_rate


@traceable(name="run_pipeline", description="Process user input, call the LLM, and return the final result for the UI.")
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
