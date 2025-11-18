import os


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)
        working_directory = os.path.abspath(working_directory)
        
        if not full_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the project root'
        
        # Create parent directories if they don't exist
        parent_dir = os.path.dirname(full_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        
        # Write content to file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {str(e)}"

