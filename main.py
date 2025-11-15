import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )
    print(response.text)

    usage = getattr(response, "usage_metadata", None)
    prompt_tokens = getattr(usage, "prompt_token_count", "Unknown") if usage else "Unknown"
    response_tokens = getattr(usage, "candidates_token_count", "Unknown") if usage else "Unknown"

    print(f"Prompt tokens: {prompt_tokens}")
    print()
    print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
