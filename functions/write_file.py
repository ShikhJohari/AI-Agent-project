import os


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)
        working_directory = os.path.abspath(working_directory)
         
        if not full_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the project root'
        
        # If the file path doesn't exist and looks like just a filename, try to find it
        if not os.path.exists(full_path) and os.sep not in file_path and file_path.count('.') <= 1:
            from functions.find_files import find_files
            
            # Extract just the filename
            filename = os.path.basename(file_path)
            search_result = find_files(working_directory, filename=filename)
            
            # Check if we found the file
            if search_result.startswith("Found"):
                # Parse the result to get the first matching path
                lines = search_result.split('\n')
                if len(lines) > 1:
                    # Get the first match (format: "  - path/to/file")
                    first_match = lines[1].strip().replace('- ', '')
                    
                    # Update the file_path to the found location
                    file_path = first_match
                    full_path = os.path.join(working_directory, file_path)
                    full_path = os.path.abspath(full_path)
        
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

