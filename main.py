import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

sys.path.insert(0, os.path.dirname(__file__))
from functions.get_files_info import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a prompt to Gemini.")
    parser.add_argument("prompt", nargs="?", help="Prompt to send to the model.")
    parser.add_argument(
        "--verbose", action="store_true", help="Print prompt and token usage details."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.prompt:
        print("Error: prompt argument required.")
        sys.exit(1)

    user_prompt = args.prompt

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    
    # Check for function calls
    function_calls = getattr(response.candidates[0].content.parts[0], 'function_call', None)
    if function_calls:
        print(f"Calling function: {function_calls.name}({dict(function_calls.args)})")
    else:
        print(response.text)

    usage = getattr(response, "usage_metadata", None)
    prompt_tokens = getattr(usage, "prompt_token_count", "Unknown") if usage else "Unknown"
    response_tokens = getattr(usage, "candidates_token_count", "Unknown") if usage else "Unknown"

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
