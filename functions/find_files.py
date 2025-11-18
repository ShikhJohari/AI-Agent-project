import os


def find_files(working_directory, filename=None, pattern=None):
    """
    Recursively search for files in the project by exact name or pattern.
    Returns a list of matching file paths relative to the project root.
    Case-insensitive matching for better user experience.
    """
    try:
        working_directory = os.path.abspath(working_directory)
        matches = []
        
        # Walk through all directories
        for root, dirs, files in os.walk(working_directory):
            # Skip common directories that should be ignored
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules', '.venv', 'venv', '.pytest_cache', '__pypackages__', 'dist', 'build', '.egg-info']]
            
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, working_directory)
                
                # Match by filename (case-insensitive)
                if filename and file.lower() == filename.lower():
                    matches.append(relative_path)
                # Match by pattern (case-insensitive substring match)
                elif pattern and pattern.lower() in file.lower():
                    matches.append(relative_path)
        
        if not matches:
            # If exact filename search failed, try pattern search as fallback
            if filename and not pattern:
                # Try pattern search with just the base name (without extension)
                base_name = os.path.splitext(filename)[0] if '.' in filename else filename
                for root, dirs, files in os.walk(working_directory):
                    dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules', '.venv', 'venv', '.pytest_cache', '__pypackages__', 'dist', 'build', '.egg-info']]
                    for file in files:
                        if base_name.lower() in file.lower():
                            full_path = os.path.join(root, file)
                            relative_path = os.path.relpath(full_path, working_directory)
                            matches.append(relative_path)
                
                if matches:
                    result_lines = [f"Exact match not found, but found {len(matches)} similar file(s):"]
                    for match in matches:
                        result_lines.append(f"  - {match}")
                    return "\n".join(result_lines)
            
            if filename:
                return f'No files found matching "{filename}" (searched case-insensitively)'
            elif pattern:
                return f'No files found matching pattern "{pattern}" (searched case-insensitively)'
            else:
                return "Please provide either 'filename' or 'pattern' parameter"
        
        # Sort matches: prioritize shorter paths (likely more relevant)
        matches.sort(key=lambda x: (len(x.split(os.sep)), x))
        
        # Return formatted results
        result_lines = [f"Found {len(matches)} file(s):"]
        for match in matches:
            result_lines.append(f"  - {match}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error searching for files: {str(e)}"
