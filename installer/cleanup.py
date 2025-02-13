import os
import shutil

def cleanup_files():
    """
    Clean up temporary installation files and logs.
    
    This function removes designated temporary directories that were created during 
    the installation process. Extend this function if additional cleanup is needed.
    """
    # List of temporary directories relative to this file's location
    base_dir = os.path.dirname(__file__)
    temp_dirs = [
        os.path.join(base_dir, "temp"),
        os.path.join(base_dir, "temp_logs")
    ]
    
    for dir_path in temp_dirs:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path, ignore_errors=True)
                print(f"Removed temporary directory: {dir_path}")
            except Exception as e:
                print(f"Error removing temporary directory {dir_path}: {e}")
    
    # Optionally, add more cleanup tasks here
    # For example, removing temporary files in other parts of the installer package.

if __name__ == "__main__":
    cleanup_files()

