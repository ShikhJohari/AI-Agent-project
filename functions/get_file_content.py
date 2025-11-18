import os
from functions.config import MAX_FILE_CHARS


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)
        working_directory = os.path.abspath(working_directory)
        
        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the project root'
        
        # If file doesn't exist at given path, try to find it
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            # Import find_files to search for the file
            from functions.find_files import find_files
            
            # Extract just the filename from the path
            filename = os.path.basename(file_path)
            search_result = find_files(working_directory, filename=filename)
            
            # Check if we found the file
            if search_result.startswith("Found"):
                # Parse the result to get the first matching path
                lines = search_result.split('\n')
                if len(lines) > 1:
                    # Get the first match (format: "  - path/to/file")
                    first_match = lines[1].strip().replace('- ', '')
                    
                    # Try reading from the found path
                    full_path = os.path.join(working_directory, first_match)
                    full_path = os.path.abspath(full_path)
                    
                    if os.path.exists(full_path) and os.path.isfile(full_path):
                        # Success! Continue with reading this file
                        pass
                    else:
                        return f'Error: File not found or is not a regular file: "{file_path}"'
                else:
                    return f'Error: File not found or is not a regular file: "{file_path}"'
            else:
                return f'Error: File not found or is not a regular file: "{file_path}". Searched entire project but could not locate "{filename}".'
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content) > MAX_FILE_CHARS:
            content = content[:MAX_FILE_CHARS]
            content += f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
        
        return content
        
    except Exception as e:
        return f"Error: {str(e)}"
