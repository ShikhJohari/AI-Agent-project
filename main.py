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
You are a highly intelligent AI coding agent with access to a Python codebase.

CORE PRINCIPLE: ALWAYS BE PROACTIVE. NEVER ask the user for file paths - YOU can find them!

When a user mentions a file without providing the full path, you MUST:
1. **AUTOMATICALLY** use find_files to locate the file (search by exact name first, then by pattern if needed)
2. Use the discovered path in subsequent operations
3. If multiple matches exist, use the most relevant one based on context
4. Only ask for clarification if there are genuinely ambiguous cases

Available operations:
- get_files_info: List files and directories
- find_files: Search for files by exact name or pattern (USE THIS PROACTIVELY!)
- get_file_content: Read file contents
- run_python_file: Execute Python files with optional arguments
- write_file: Write or overwrite files

SMART FILE HANDLING EXAMPLES:
- User says "read readme.md" → IMMEDIATELY call find_files(filename="README.md") or find_files(pattern="readme"), then read the found file
- User says "add docstrings to my config file" → find_files(pattern="config"), examine results, read the file, make changes
- User says "run the tests" → find_files(pattern="test"), identify test files, run them
- User says "modify calculator.py" → find_files(filename="calculator.py"), find it, read it, make changes

CRITICAL RULES:
1. NEVER say "I need the path" - YOU find it using find_files!
2. File names are case-insensitive - search flexibly (readme.md, README.md, Readme.MD are all the same)
3. Always search before claiming a file doesn't exist
4. Be smart about common variations (.py, .txt, .md extensions, etc.)
5. Think like a developer - understand project structure and conventions

Your goal is to be so intelligent that users feel like they're working with a mind-reading assistant, not a rigid script.
"""


def call_function(function_call_part, verbose=False):
    # Import the actual function implementations
    from functions.get_file_content import get_file_content
    from functions.get_files_info import get_files_info
    from functions.run_python_file import run_python_file
    from functions.write_file import write_file
    from functions.find_files import find_files
    
    # Create a mapping of function names to functions
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
        "find_files": find_files,
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
    
    # Add working_directory to args (project root = where main.py is located)
    args_dict = dict(function_call_part.args)
    project_root = os.path.dirname(os.path.abspath(__file__))
    args_dict["working_directory"] = project_root
    
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

    # If no prompt provided, launch interactive CLI
    if not args.prompt:
        try:
            from interactive_cli import interactive_loop
            interactive_loop()
            return
        except ImportError as e:
            print(f"Error: Could not load interactive CLI: {e}")
            sys.exit(1)

    user_prompt = args.prompt

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    max_iterations = 20
    
    for iteration in range(max_iterations):
        try:
            # Generate content with the entire messages list
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            
            # Add all candidates' content to messages
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
            
            # Check if model is finished (no function calls and has text)
            has_function_call = False
            has_text = False
            
            for candidate in response.candidates:
                if not candidate.content or not candidate.content.parts:
                    continue
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        has_function_call = True
                        # Call the function
                        function_call_result = call_function(part.function_call, verbose=args.verbose)
                        
                        # Validate that the result has the expected structure
                        if not hasattr(function_call_result.parts[0], 'function_response') or \
                           not hasattr(function_call_result.parts[0].function_response, 'response'):
                            raise RuntimeError("Function call result does not have expected structure")
                        
                        # Print the result if verbose
                        if args.verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                        
                        # Add function response to messages with role "user"
                        messages.append(function_call_result)
                    
                    if hasattr(part, 'text') and part.text:
                        has_text = True
            
            # If no function calls and has text, we're done
            if not has_function_call and has_text:
                print(response.text)
                break
                
        except Exception as e:
            print(f"Error during iteration {iteration + 1}: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            break
    else:
        # Loop completed without breaking (max iterations reached)
        print("Warning: Maximum iterations reached without completing the task.")

    if args.verbose:
        print(f"\nUser prompt: {user_prompt}")
        usage = getattr(response, "usage_metadata", None)
        if usage:
            prompt_tokens = getattr(usage, "prompt_token_count", "Unknown")
            response_tokens = getattr(usage, "candidates_token_count", "Unknown")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
