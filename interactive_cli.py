#!/usr/bin/env python3
"""Interactive CLI for the AI Coding Agent."""

import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))
from functions.get_files_info import available_functions

# Initialize
load_dotenv()
console = Console()

# Gemini client setup
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    console.print("[bold red]Error:[/bold red] GEMINI_API_KEY not found in environment")
    console.print("Please set your API key in the .env file")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# System prompt
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


def get_greeting():
    """Get time-appropriate greeting."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


def show_welcome():
    """Display welcome message."""
    greeting = get_greeting()
    
    welcome_text = Text()
    welcome_text.append(f"{greeting}! ", style="bold cyan")
    welcome_text.append("Welcome to ", style="white")
    welcome_text.append("Kodex", style="bold magenta")
    
    info_text = Text()
    info_text.append("\nI'm your intelligent coding assistant. I can:\n", style="dim")
    info_text.append("  • Find and read files automatically\n", style="green")
    info_text.append("  • Write and modify code\n", style="green")
    info_text.append("  • Run Python scripts\n", style="green")
    info_text.append("  • Debug and refactor code\n", style="green")
    info_text.append("\nType ", style="dim")
    info_text.append("exit", style="bold yellow")
    info_text.append(", ", style="dim")
    info_text.append("quit", style="bold yellow")
    info_text.append(", or ", style="dim")
    info_text.append("q", style="bold yellow")
    info_text.append(" to leave. Press ", style="dim")
    info_text.append("Ctrl+C", style="bold yellow")
    info_text.append(" anytime.\n", style="dim")
    
    panel = Panel(
        welcome_text.append("\n").append(info_text),
        border_style="cyan",
        padding=(1, 2),
    )
    
    console.print()
    console.print(panel)
    console.print()


def call_function(function_call_part, show_details=False):
    """Execute a function call from the agent."""
    from functions.get_file_content import get_file_content
    from functions.get_files_info import get_files_info
    from functions.run_python_file import run_python_file
    from functions.write_file import write_file
    from functions.find_files import find_files
    
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
        "find_files": find_files,
    }
    
    function_name = function_call_part.name
    
    # Show function call
    if show_details:
        console.print(f"[dim]  → Calling: {function_name}({function_call_part.args})[/dim]")
    else:
        console.print(f"[dim cyan]  • {function_name}[/dim cyan]")
    
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
    project_root = os.path.dirname(os.path.abspath(__file__))
    args_dict["working_directory"] = project_root
    
    # Call the function
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


def execute_query(user_prompt, messages, show_details=False):
    """Execute a single query and return updated messages."""
    # Add user prompt to messages
    messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))
    
    max_iterations = 20
    final_response = None
    
    for iteration in range(max_iterations):
        try:
            # Generate content
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                ),
            )
            
            # Add response to messages
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
            
            # Process response
            has_function_call = False
            has_text = False
            
            for candidate in response.candidates:
                if not candidate.content or not candidate.content.parts:
                    continue
                    
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        has_function_call = True
                        function_call_result = call_function(part.function_call, show_details)
                        messages.append(function_call_result)
                    
                    if hasattr(part, 'text') and part.text:
                        has_text = True
            
            # If done, return the response
            if not has_function_call and has_text:
                final_response = response.text
                break
                
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            if show_details:
                import traceback
                traceback.print_exc()
            break
    
    if final_response is None and iteration == max_iterations - 1:
        final_response = "Maximum iterations reached. The task may be incomplete."
    
    return final_response, messages


def interactive_loop():
    """Main interactive loop."""
    show_welcome()
    
    # Initialize conversation context
    messages = []
    show_details = False
    
    # Check for verbose environment variable
    if os.environ.get("AGENT_VERBOSE", "").lower() in ["1", "true", "yes"]:
        show_details = True
    
    while True:
        try:
            # Get user input
            console.print()
            user_input = Prompt.ask(
                "[bold cyan]Enter prompt here[/bold cyan]",
                default=""
            ).strip()
            
            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "q", "bye"]:
                console.print("\n[cyan]Goodbye! Happy coding! 👋[/cyan]\n")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Special commands
            if user_input.lower() == "clear":
                console.clear()
                show_welcome()
                continue
            
            if user_input.lower() == "reset":
                messages = []
                console.print("[yellow]Context cleared. Starting fresh![/yellow]")
                continue
            
            if user_input.lower() == "verbose":
                show_details = not show_details
                status = "enabled" if show_details else "disabled"
                console.print(f"[yellow]Verbose mode {status}[/yellow]")
                continue
            
            # Execute the query with a spinner
            console.print()
            with Live(Spinner("dots", text="[cyan]Thinking...[/cyan]"), console=console, transient=True):
                response, messages = execute_query(user_input, messages, show_details)
            
            # Display response
            if response:
                console.print()
                console.print(Panel(
                    Markdown(response),
                    border_style="green",
                    padding=(1, 2),
                ))
            
        except KeyboardInterrupt:
            console.print("\n\n[cyan]Goodbye! Happy coding! 👋[/cyan]\n")
            break
        except EOFError:
            console.print("\n\n[cyan]Goodbye! Happy coding! 👋[/cyan]\n")
            break


def main():
    """Entry point for interactive CLI."""
    try:
        interactive_loop()
    except Exception as e:
        console.print(f"\n[bold red]Fatal error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

