import subprocess
import os

def install_tool(tool):
    """
    Execute the installation script for a tool.
    This function runs the tool's installation script using subprocess.
    It returns True if the installation succeeds, otherwise False.
    """
    # Determine the full path of the installation script
    script_path = os.path.join(os.path.dirname(__file__), tool["script"])
    
    if not os.path.exists(script_path):
        print(f"Installation script not found: {script_path}")
        return False

    try:
        if os.name == 'nt':
            # On Windows, run the script using the command interpreter
            subprocess.check_call(["cmd", "/c", script_path])
        else:
            # On Unix-like systems, assume the script is a bash script
            subprocess.check_call(["bash", script_path])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Installation failed for {tool['name']} using {script_path}. Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error installing {tool['name']}: {e}")
        return False

def validate_installation(tool):
    """
    Validate the installation of a tool by running its validation command.
    This function returns True if the validation command output contains 'version', otherwise False.
    """
    try:
        output = subprocess.check_output(tool["validation_cmd"].split(), stderr=subprocess.STDOUT)
        if b"version" in output.lower():
            return True
        else:
            print(f"Validation output for {tool['name']} did not contain 'version'. Output: {output}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Validation command failed for {tool['name']}. Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during validation for {tool['name']}: {e}")
        return False

