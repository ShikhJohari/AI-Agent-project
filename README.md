# AI Coding Agent with Gemini

A powerful AI coding assistant powered by Google's Gemini 2.5 Flash that can interact with your codebase through function calling. The agent operates in a sandboxed environment, allowing it to safely read, write, execute, and analyze code within a specified working directory.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Core Concepts](#core-concepts)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Functions](#available-functions)
- [Security Features](#security-features)
- [Real-World Use Cases](#real-world-use-cases)
- [Example Interactions](#example-interactions)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Limitations](#limitations)

## 🎯 Overview

This AI agent is designed to be a helpful coding assistant that can understand natural language requests and execute actions on your codebase. Unlike simple chatbots, this agent can:

- **Read** files and directories in your project
- **Write** new files or modify existing ones
- **Execute** Python scripts with custom arguments
- **Analyze** code structure and provide insights

All operations are constrained to a predefined working directory for security, making it safe to use in production environments.

## 🏗️ Architecture

### High-Level Flow

```
User Prompt → AI Agent → Function Planning → Function Execution → Results → AI Response
                ↑                                                              ↓
                └─────────────────── Iterative Loop ────────────────────────┘
```

### Components

1. **Main Agent (`main.py`)**: The orchestrator that handles communication with Gemini AI
2. **Function Declarations (`functions/get_files_info.py`)**: Schema definitions for available tools
3. **Function Implementations**: Individual modules for each capability
4. **Working Directory**: Sandboxed environment (default: `./calculator`)
5. **Sample Project**: Calculator application demonstrating agent capabilities

## 💡 Core Concepts

### 1. Function Calling

The agent uses Gemini's function calling feature to convert natural language into structured function calls. When you ask "What files are in my project?", the AI:

1. Analyzes your request
2. Determines the appropriate function (`get_files_info`)
3. Generates the parameters
4. Executes the function
5. Interprets the results
6. Responds in natural language

### 2. Sandboxed Execution

All file operations are restricted to the working directory (`./calculator` by default). This prevents:

- Access to files outside the designated folder
- Execution of system commands
- Unauthorized file modifications
- Path traversal attacks

### 3. Iterative Problem Solving

The agent can perform multiple function calls in sequence to solve complex tasks. For example, to "fix all bugs in tests.py":

1. Read the test file
2. Execute tests to see failures
3. Read the source code
4. Identify issues
5. Modify the source code
6. Re-run tests to verify

### 4. Context Management

The agent maintains conversation history across function calls, allowing it to:

- Remember previous actions
- Build on earlier context
- Make informed decisions
- Provide coherent responses

## ✨ Features

### 🔍 Code Analysis
- List all files and directories with sizes
- Read file contents (with truncation for large files)
- Understand code structure and dependencies

### ✍️ Code Modification
- Create new files
- Modify existing files
- Write entire modules or functions

### ▶️ Code Execution
- Run Python scripts
- Pass command-line arguments
- Capture stdout, stderr, and exit codes
- 30-second timeout protection

### 🧠 Intelligent Assistance
- Debug code issues
- Write tests
- Refactor code
- Add documentation
- Implement features

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- Google Gemini API key

### Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd AI-Agent-project
```

2. **Install dependencies:**
```bash
# Using pip
pip install google-genai==1.12.1 python-dotenv==1.1.0

# Or using uv (if available)
uv sync
```

3. **Set up environment variables:**
Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_api_key_here
```

To get a Gemini API key:
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Sign in with your Google account
- Generate a new API key

## ⚙️ Configuration

### Working Directory

By default, the agent operates in the `./calculator` directory. To change this, modify line 65 in `main.py`:

```python
args_dict["working_directory"] = "./your-directory"
```

### File Size Limit

Large files are truncated to prevent token overflow. Adjust the limit in `functions/config.py`:

```python
MAX_FILE_CHARS = 10000  # Characters, not bytes
```

### Execution Timeout

Python scripts timeout after 30 seconds. Modify in `functions/run_python_file.py`:

```python
timeout=30  # Seconds
```

### Model Selection

Change the Gemini model in `main.py`:

```python
model="gemini-2.5-flash-lite"  # or gemini-2.0-flash, gemini-1.5-pro, etc.
```

## 🚀 Usage

### Basic Syntax

```bash
python main.py "<your prompt>"
```

### Verbose Mode

Get detailed information about function calls and token usage:

```bash
python main.py "<your prompt>" --verbose
```

### Example Commands

**List files:**
```bash
python main.py "What files are in my project?"
```

**Read a file:**
```bash
python main.py "Show me the contents of main.py"
```

**Run tests:**
```bash
python main.py "Run the tests.py file"
```

**Execute with arguments:**
```bash
python main.py "Run main.py with the expression '5 + 3'"
```

**Write code:**
```bash
python main.py "Create a new file called helper.py with a function that squares a number"
```

**Debug:**
```bash
python main.py "The tests are failing. Can you fix the bugs?"
```

**Complex tasks:**
```bash
python main.py "Add a power operation to the calculator and write tests for it"
```

## 🔧 Available Functions

### 1. `get_files_info`

Lists files and directories with metadata.

**Parameters:**
- `directory` (optional): Path relative to working directory (default: ".")

**Returns:**
- List of files with sizes and type (file/directory)

**Example:**
```
- main.py: file_size=842 bytes, is_dir=False
- pkg: file_size=128 bytes, is_dir=True
- tests.py: file_size=1256 bytes, is_dir=False
```

### 2. `get_file_content`

Reads and returns file contents.

**Parameters:**
- `file_path` (required): Path to file relative to working directory

**Returns:**
- File contents as string (truncated if > MAX_FILE_CHARS)

**Features:**
- UTF-8 encoding
- Automatic truncation warning
- Error handling for missing files

### 3. `run_python_file`

Executes a Python script and captures output.

**Parameters:**
- `file_path` (required): Path to .py file relative to working directory
- `args` (optional): List of command-line arguments

**Returns:**
- STDOUT, STDERR, and exit code

**Features:**
- 30-second timeout
- Working directory set to sandbox
- Non-.py files rejected

### 4. `write_file`

Creates or overwrites a file with content.

**Parameters:**
- `file_path` (required): Path to file relative to working directory
- `content` (required): String content to write

**Returns:**
- Success message with character count

**Features:**
- Creates parent directories automatically
- UTF-8 encoding
- Overwrites existing files without warning

## 🔒 Security Features

### Path Traversal Protection

All functions validate that paths stay within the working directory:

```python
# ✅ Allowed
file_path = "src/module.py"
file_path = "tests/test_main.py"

# ❌ Blocked
file_path = "../../../etc/passwd"
file_path = "/absolute/path/file.py"
```

### File Type Validation

Only `.py` files can be executed, preventing:
- Shell script execution
- Binary execution
- Arbitrary command injection

### Timeout Protection

Scripts are terminated after 30 seconds to prevent:
- Infinite loops
- Resource exhaustion
- Denial of service

### Automatic Working Directory Injection

The working directory is injected server-side, not from AI responses:

```python
# User/AI never directly controls working_directory
args_dict["working_directory"] = "./calculator"
```

### Read-Only API Key

The API key is loaded from environment variables, never exposed to the AI or user.

## 🌍 Real-World Use Cases

### 1. Code Review Assistant

```bash
python main.py "Review all Python files and suggest improvements"
```

The agent can:
- Identify code smells
- Suggest refactoring
- Check for best practices
- Find potential bugs

### 2. Test Generator

```bash
python main.py "Generate comprehensive unit tests for calculator.py"
```

The agent can:
- Analyze function signatures
- Create test cases for edge cases
- Write assertions
- Run and verify tests

### 3. Bug Fixer

```bash
python main.py "The calculator fails on division by zero. Fix it and add proper error handling"
```

The agent can:
- Read the code
- Identify the issue
- Implement a fix
- Test the solution

### 4. Documentation Writer

```bash
python main.py "Add docstrings to all functions in calculator.py following Google style"
```

The agent can:
- Analyze function signatures
- Write descriptive docstrings
- Include parameter types and return values
- Add usage examples

### 5. Feature Implementation

```bash
python main.py "Add support for parentheses in mathematical expressions"
```

The agent can:
- Understand requirements
- Modify existing code
- Add new functionality
- Update tests

### 6. Code Refactoring

```bash
python main.py "Refactor the calculator to use a visitor pattern"
```

The agent can:
- Understand design patterns
- Restructure code
- Maintain functionality
- Update all dependencies

### 7. Migration Assistant

```bash
python main.py "Convert all print statements to use logging instead"
```

The agent can:
- Find all occurrences
- Replace with proper logging calls
- Add necessary imports
- Configure logging setup

## 📚 Example Interactions

### Example 1: Basic Information Gathering

**Prompt:**
```bash
python main.py "Tell me about the calculator project"
```

**Agent Actions:**
1. Calls `get_files_info(".")` to see project structure
2. Calls `get_file_content("README.md")` if available
3. Calls `get_file_content("main.py")` to understand entry point

**Response:**
> The calculator project is a simple mathematical expression evaluator. It has a Calculator class that supports basic operations (+, -, *, /) with proper operator precedence. The main.py file provides a CLI interface...

### Example 2: Running and Debugging

**Prompt:**
```bash
python main.py "Run the tests and fix any failures"
```

**Agent Actions:**
1. Calls `run_python_file("tests.py")`
2. Analyzes failures
3. Calls `get_file_content("pkg/calculator.py")`
4. Identifies bug
5. Calls `write_file("pkg/calculator.py", fixed_content)`
6. Calls `run_python_file("tests.py")` to verify

**Response:**
> I found a bug in the division operation. The calculator wasn't handling division properly. I've fixed it and all tests now pass!

### Example 3: Feature Addition

**Prompt:**
```bash
python main.py "Add a modulo operation to the calculator"
```

**Agent Actions:**
1. Calls `get_file_content("pkg/calculator.py")`
2. Understands current implementation
3. Calls `write_file("pkg/calculator.py", updated_content)` with modulo support
4. Calls `get_file_content("tests.py")`
5. Calls `write_file("tests.py", updated_tests)` to add tests
6. Calls `run_python_file("tests.py")` to verify

**Response:**
> I've added modulo (%) operation to the calculator. The operation has been integrated into the Calculator class with proper precedence (same as division). I also added tests to verify it works correctly. All tests pass!

## 📁 Project Structure

```
AI-Agent-project/
├── main.py                 # Main agent orchestrator
├── pyproject.toml         # Project dependencies
├── tests.py               # Agent function tests
├── README.md              # This file
│
├── functions/             # Agent function implementations
│   ├── config.py         # Configuration constants
│   ├── get_files_info.py # List & schema definitions
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
│
└── calculator/           # Sample project (working directory)
    ├── main.py          # Calculator CLI
    ├── tests.py         # Calculator tests
    ├── README.md        # Calculator docs
    └── pkg/
        ├── calculator.py # Core calculator logic
        └── render.py     # Output formatting
```

## 🧪 Testing

### Test Agent Functions

Run the test suite to verify all functions work correctly:

```bash
python tests.py
```

This tests:
- File execution with/without arguments
- Path traversal prevention
- Invalid file handling
- Error cases

### Test Calculator

Run the calculator's test suite:

```bash
cd calculator
python tests.py
```

Or use the agent:

```bash
python main.py "Run the calculator tests"
```

### Test Agent Capabilities

Try these prompts to test the agent:

```bash
# Information gathering
python main.py "What files exist in pkg directory?"

# Code reading
python main.py "Show me the Calculator class"

# Execution
python main.py "Calculate 15 divided by 3"

# Writing
python main.py "Create a file called notes.txt with 'Hello World'"

# Complex task
python main.py "Add comments to all functions in calculator.py"
```

## ⚠️ Limitations

### 1. Context Window

While the agent can handle multiple iterations, very complex tasks may require:
- Breaking into smaller prompts
- Explicit step-by-step instructions

### 2. File Size

Files are truncated at `MAX_FILE_CHARS` (default: 10,000 characters). For larger files:
- Increase the limit in `config.py`
- Ask the agent to focus on specific sections

### 3. Execution Timeout

Scripts must complete within 30 seconds. For longer-running tasks:
- Increase timeout in `run_python_file.py`
- Avoid infinite loops or heavy computations

### 4. Python Only

Currently only Python files can be executed. To support other languages:
- Add new function declarations
- Implement language-specific execution functions

### 5. No Multi-File Edits

The agent modifies one file at a time. For large refactorings:
- Guide it through multiple steps
- Be explicit about file order

### 6. Working Directory Constraint

All operations are limited to one working directory. To work with multiple projects:
- Change the working directory in code
- Run separate agent instances

### 7. API Costs

Gemini API calls incur costs. Use `--verbose` to monitor token usage:
- Each function call adds tokens
- Large files increase context size
- Iterative tasks accumulate costs

## 🔄 Extending the Agent

### Adding New Functions

1. **Define the schema** in `functions/get_files_info.py`:
```python
schema_new_function = types.FunctionDeclaration(
    name="new_function",
    description="What this function does",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "param": types.Schema(
                type=types.Type.STRING,
                description="Parameter description",
            ),
        },
        required=["param"],
    ),
)
```

2. **Add to available functions**:
```python
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        schema_new_function,  # Add here
    ]
)
```

3. **Implement the function** in a new file:
```python
def new_function(working_directory, param):
    # Implementation
    pass
```

4. **Register in main.py**:
```python
from functions.new_function import new_function

function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
    "new_function": new_function,  # Add here
}
```

### Changing the Working Directory

Modify line 65 in `main.py` to point to your project:

```python
args_dict["working_directory"] = "/path/to/your/project"
```

### Using Different AI Models

Change the model in `main.py`:

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",  # or gemini-1.5-pro, gemini-1.5-flash
    # ...
)
```

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

- Built with [Google Gemini AI](https://ai.google.dev/)
- Inspired by autonomous coding agents and AI assistants

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review example interactions

---

**Happy Coding with AI! 🚀**

