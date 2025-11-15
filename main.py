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


def call_function(function_call_part, verbose=False):
    # Import the actual function implementations
    from functions.get_file_content import get_file_content
    from functions.get_files_info import get_files_info
    from functions.run_python_file import run_python_file
    from functions.write_file import write_file
    
    # Create a mapping of function names to functions
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    function_name = function_call_part.name
    
    # Print based on verbose flag
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function name is valid
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Add working_directory to args
    args_dict = dict(function_call_part.args)
    args_dict["working_directory"] = "./calculator"
    
    # Call the function and return result
    function_result = function_map[function_name](**args_dict)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


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
        function_call_result = call_function(function_calls, verbose=args.verbose)
        
        # Validate that the result has the expected structure
        if not hasattr(function_call_result.parts[0], 'function_response') or \
           not hasattr(function_call_result.parts[0].function_response, 'response'):
            raise RuntimeError("Function call result does not have expected structure")
        
        # Print the result if verbose
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
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
