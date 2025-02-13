# Troubleshooting Guide

This document provides guidance for resolving common issues that may occur during the installation of forensic tools using the Forensic Tools Installer.

---

## Common Issues & Solutions

### 1. Configuration Errors
- **Issue:**  
  The installer fails to load `config.json`.
- **Solution:**  
  - Ensure that the `config.json` file exists in the `installer` directory.
  - Verify that the JSON format is correct. You can use an online JSON validator.
  - Check file permissions to ensure that the installer can read the file.

### 2. Installation Script Failures
- **Issue:**  
  A tool's installation script (e.g., `install.sh`) returns an error.
- **Solution:**  
  - Confirm that you have the necessary administrative privileges (run as root or with `sudo` on Linux/macOS).
  - Open a terminal and run the installation script manually to view any error messages:
    ```bash
    bash path/to/install.sh
    ```
  - Ensure that all dependencies and required system packages are installed.
  - Verify that the source directory (`tool_files`) exists and contains all necessary files.

### 3. Validation Failures
- **Issue:**  
  The installer reports that a tool failed validation (e.g., missing or incorrect version output).
- **Solution:**  
  - Check that the tool’s executable is correctly installed and accessible from the PATH.
  - Run the validation command manually to see the output:
    ```bash
    forensic_tool_one --version
    ```
  - Confirm that the validation command in `config.json` accurately reflects the correct command and expected output.
  - Review any console output or log files for additional error details.

### 4. GUI Freezes or Unresponsive
- **Issue:**  
  The installer GUI becomes unresponsive during installation.
- **Solution:**  
  - Ensure that you are running the installer in an environment that supports Tkinter.
  - Check that the installation routines are running in a separate thread (as implemented) to keep the GUI responsive.
  - Look for any blocking calls in the code and consider refactoring them to maintain responsiveness.

### 5. Cleanup Not Executed
- **Issue:**  
  Temporary files or logs remain after the installation completes.
- **Solution:**  
  - Verify that the `cleanup_files()` function in `cleanup.py` is being called at the end of the installation process.
  - Manually inspect the directories listed in the cleanup function and ensure that permissions allow for deletion.
  - Check the console output for any error messages during cleanup.

---

## General Debugging Tips

- **Run Installer from Terminal:**  
  Running the installer from a terminal or command prompt can help capture detailed error messages.
  
- **Check Logs:**  
  Refer to any generated log files in the `tests/logs/` directory for additional context on failures.

- **Update Environment Variables:**  
  If the PATH is not updated correctly, manually add the installation directory to your PATH and source your profile:
  ```bash
  export PATH=$PATH:/usr/local/forensic_tool_one
  source ~/.bashrc
  ```

- **Community and Support:**  
  If you continue to experience issues, contact support at [support@example.com] with the error details and log output.

---

By following this troubleshooting guide, you should be able to resolve common issues encountered during installation. For further assistance, please consult the project documentation or reach out to the support team.
```

---

