import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


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
    )
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
