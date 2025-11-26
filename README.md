# Kodex

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

**NEW: Beautiful Interactive Mode!** 🎨 Just run `./agent` to start a continuous conversation with your AI assistant. No more typing long commands—enjoy a smooth, colorful, context-aware experience.

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

### 🎨 Interactive CLI Mode (NEW!)
- **Beautiful terminal UI** - Rich colors, panels, and formatted output
- **Time-aware greeting** - Good morning/afternoon/evening based on your time
- **Continuous conversation** - Ask multiple questions in one session
- **Context preservation** - Maintains full conversation history using the model's context window
- **Smart prompts** - Clear "Enter prompt here:" message for easy interaction
- **Special commands** - clear, reset, verbose, exit
- **Graceful exit** - Multiple exit options (exit, quit, q, Ctrl+C)
- **Zero friction** - Just type `./agent` and start coding!

**Example:** Run `./agent` once and have a natural conversation with your AI assistant!

### 🎯 Smart File Discovery
- **Automatic file finding** - No need to specify full paths!
- **Case-insensitive search** - "readme.md", "README.MD", "Readme.md" all work
- **Pattern matching** - Find files by partial names or extensions
- **Intelligent fallback** - Automatically searches when exact matches fail
- **Nested file detection** - Finds files in any subdirectory
- **Sorted by relevance** - Most relevant files appear first

**Example:** Just say "show me config.py" and the agent will find it anywhere in your project, no matter where it's located!

### 🔍 Code Analysis
- List all files and directories with sizes
- Read file contents (with truncation for large files)
- Understand code structure and dependencies
- Search for files by exact name or pattern

### ✍️ Code Modification
- Create new files
- Modify existing files
- Write entire modules or functions
- Auto-locate files before writing

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
pip install google-genai==1.12.1 python-dotenv==1.1.0 rich>=13.7.0

# Or using uv (recommended - automatically installs all dependencies)
uv sync
```

3. **Set up environment variables:**
Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_api_key_here
```

4. **Make the agent launcher executable (optional but recommended):**
```bash
chmod +x agent
```

Now you can start the interactive agent with just:
```bash
./agent
```

**Optional: Add to PATH for system-wide access:**
```bash
# Add to your ~/.bashrc or ~/.zshrc
export PATH="$PATH:/path/to/AI-Agent-project"

# Or create a symlink
sudo ln -s /path/to/AI-Agent-project/agent /usr/local/bin/agent

# Then use it from anywhere:
agent
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

### Interactive Mode (Recommended!) ⭐

The easiest way to use the agent is through the beautiful interactive CLI:

```bash
./agent
```

Or alternatively:

```bash
python main.py
```

**Features:**
- **Time-based greeting** - Good morning/afternoon/evening based on your local time
- **Continuous conversation** - Ask multiple questions without restarting
- **Context preservation** - Maintains full conversation history
- **Beautiful UI** - Colored output, panels, and markdown rendering
- **Smart prompts** - Clear "Enter prompt here:" message
- **Exit commands** - Type `exit`, `quit`, `q`, or press `Ctrl+C`

**Special commands in interactive mode:**
- `clear` - Clear screen and show welcome again
- `reset` - Clear conversation context and start fresh
- `verbose` - Toggle detailed function call information
- `exit`, `quit`, `q` - Exit the interactive session

**Example session:**
```
$ ./agent

╭──────────────────────────────────────────────────────────╮
│                                                          │
│  Good morning! Welcome to the AI Coding Agent 🤖         │
│                                                          │
│  I'm your intelligent coding assistant. I can:           │
│    • Find and read files automatically                   │
│    • Write and modify code                               │
│    • Run Python scripts                                  │
│    • Debug and refactor code                             │
│                                                          │
│  Type exit, quit, or q to leave. Press Ctrl+C anytime.   │
│                                                          │
╰──────────────────────────────────────────────────────────╯

Enter prompt here: show me my readme file
  • find_files
  • get_file_content

╭──────────────────────────────────────────────────────────╮
│                                                          │
│  [Response with README contents displayed beautifully]   │
│                                                          │
╰──────────────────────────────────────────────────────────╯

Enter prompt here: what tests do we have?
  • find_files

╭──────────────────────────────────────────────────────────╮
│                                                          │
│  [Lists test files found in the project]                 │
│                                                          │
╰──────────────────────────────────────────────────────────╯

Enter prompt here: exit

Goodbye! Happy coding! 👋
```

### Single-Command Mode

For quick one-off queries, use the original single-command syntax:

```bash
python main.py "<your prompt>"
```

### Verbose Mode

Get detailed information about function calls and token usage:

```bash
python main.py "<your prompt>" --verbose
```

### Example Commands

**🎯 Smart File Finding (No pa
[...File "README.md" truncated at 10000 characters]