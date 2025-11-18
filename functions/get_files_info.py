import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes. Works anywhere in the project.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the project root (e.g., '.', 'calculator', 'functions', 'calculator/pkg'). If not provided, lists files in the project root.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file anywhere in the project.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the project root (e.g., 'main.py', 'calculator/main.py', 'functions/config.py').",
            ),
        },
        required=["file_path"],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments. Can run any .py file in the project.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the project root (e.g., 'tests.py', 'calculator/main.py', 'calculator/tests.py').",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file anywhere in the project. Creates the file and parent directories if they don't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the project root (e.g., 'newfile.py', 'calculator/utils.py', 'functions/helper.py').",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        full_path = os.path.abspath(full_path)
        working_directory = os.path.abspath(working_directory)
        
        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the project root'
        
        if not os.path.exists(full_path):
            return f'Error: "{directory}" does not exist'
        
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        entries = os.listdir(full_path)
        entries.sort()
        
        result_lines = []
        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            try:
                file_size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                result_lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
            except OSError as e:
                result_lines.append(f"- {entry}: Error accessing file: {e}")
        
        return "\n".join(result_lines) if result_lines else "Directory is empty"
        
    except Exception as e:
        return f"Error: {str(e)}"
