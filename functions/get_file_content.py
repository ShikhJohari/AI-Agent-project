import os
from functions.config import MAX_FILE_CHARS


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)
        working_directory = os.path.abspath(working_directory)
        
        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the project root'
        
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content) > MAX_FILE_CHARS:
            content = content[:MAX_FILE_CHARS]
            content += f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
        
        return content
        
    except Exception as e:
        return f"Error: {str(e)}"
