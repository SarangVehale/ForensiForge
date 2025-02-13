# Forensic Tools Installer

## Overview

The Forensic Tools Installer is a self-contained installation package for a suite of forensic tools. It provides a user-friendly GUI for both full and selective installations. After the installation is complete, the installer automatically cleans up temporary files, leaving only the installed tools on your system.

## Directory Structure

```
forensic-installer/
├── docs/
│   ├── README.md             # Project overview and instructions
│   ├── TOOL_DESCRIPTIONS.md  # Detailed descriptions of each forensic tool
│   └── TROUBLESHOOTING.md    # Common issues and their solutions
├── installer/
│   ├── main_installer.py     # Main entry point with the GUI interface
│   ├── install_utils.py      # Utility functions for installation and validation
│   ├── cleanup.py            # Cleanup routines to remove temporary files
│   └── config.json           # Configuration file with tool metadata
├── tools/
│   ├── tool1/
│   │   ├── install.sh        # Installation script for Forensic Tool One
│   │   └── tool_files/       # Binaries and supporting files for Tool One
│   ├── tool2/
│   │   ├── install.sh        # Installation script for Forensic Tool Two
│   │   └── tool_files/       # Binaries and supporting files for Tool Two
└── tests/
    ├── test_installation.sh  # Script for automated testing of installations
    └── logs/                 # Log files from test runs
```

## Installation Instructions

1. **Prerequisites:**
   - **Python 3.x** must be installed on your system.
   - For Linux/macOS: Bash is required.
   - For Windows: Ensure you have a compatible shell environment (e.g., using WSL or adapting the scripts for Windows).
   - Administrative privileges may be required for installing tools into system directories.

2. **Running the Installer:**
   - Extract the ZIP file to your desired location.
   - Open a terminal or command prompt and navigate to the `installer` directory.
   - Run the installer:
     - **Linux/macOS:** `python3 main_installer.py`
     - **Windows:** `python main_installer.py` (ensure Python is added to your PATH)

3. **Using the Installer:**
   - The GUI will display two installation options:
     - **Full Installation:** Installs all available forensic tools.
     - **Selective Installation:** Allows you to choose specific tools via checkboxes.
   - Follow the on-screen instructions. The installer displays progress and status messages.
   - Once installation is complete, the installer automatically cleans up temporary files.

## Troubleshooting

- If the installation fails for any tool, check the console output or log files in the `tests/logs/` directory.
- Consult the [TROUBLESHOOTING](./TROUBLESHOOTING.md) guide for common issues and solutions.
- Ensure that you have the necessary permissions to install software on your system.

## Contact & Support

For further assistance or inquiries, please contact the development team at [support@example.com].

--
