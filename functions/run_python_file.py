import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)
        working_directory = os.path.abspath(working_directory)
        
        # Check if file_path is outside working_directory
        if not full_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the project root'
        
        # Check if file exists - if not, try to find it
        if not os.path.exists(full_path):
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
                    
                    # Update file_path and full_path with found location
                    file_path = first_match
                    full_path = os.path.join(working_directory, first_match)
                    full_path = os.path.abspath(full_path)
                    
                    if not os.path.exists(full_path):
                        return f'Error: File "{file_path}" not found.'
                else:
                    return f'Error: File "{file_path}" not found.'
            else:
                return f'Error: File "{file_path}" not found. Searched entire project but could not locate "{filename}".'
        
        # Check if file is a Python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Run the Python file
        cmd = ['python3', full_path] + args
        completed_process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory
        )
        
        # Format the output
        output_parts = []
        
        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")
        
        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr}")
        
        # Check if process exited with non-zero code
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
        
        # Return formatted output or "No output produced."
        if output_parts:
            return "\n".join(output_parts)
        else:
            return "No output produced."
        
    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"

