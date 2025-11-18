import os


def find_files(working_directory, filename=None, pattern=None):
    """
    Recursively search for files in the project by exact name or pattern.
    Returns a list of matching file paths relative to the project root.
    """
    try:
        working_directory = os.path.abspath(working_directory)
        matches = []
        
        # Walk through all directories
        for root, dirs, files in os.walk(working_directory):
            # Skip common directories that should be ignored
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules', '.venv', 'venv', '.pytest_cache', '__pypackages__']]
            
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, working_directory)
                
                # Match by exact filename
                if filename and file == filename:
                    matches.append(relative_path)
                # Match by pattern (simple substring match)
                elif pattern and pattern.lower() in file.lower():
                    matches.append(relative_path)
        
        if not matches:
            if filename:
                return f'No files found with exact name "{filename}"'
            elif pattern:
                return f'No files found matching pattern "{pattern}"'
            else:
                return "Please provide either 'filename' or 'pattern' parameter"
        
        # Return formatted results
        result_lines = [f"Found {len(matches)} file(s):"]
        for match in matches:
            result_lines.append(f"  - {match}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error searching for files: {str(e)}"
