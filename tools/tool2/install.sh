#!/bin/bash
# ------------------------------------------------------------------
# Forensic Tool Two Installation Script
# ------------------------------------------------------------------
# This script installs Forensic Tool Two by copying the necessary
# files to the installation directory, setting appropriate permissions,
# and updating the user’s environment if necessary.
# ------------------------------------------------------------------

# Define the installation directory (modify as needed)
INSTALL_DIR="/usr/local/forensic_tool_two"

echo "Starting installation of Forensic Tool Two..."

# Check if running as root (if necessary for the installation directory)
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or use sudo to install Forensic Tool Two."
  exit 1
fi

# Create the installation directory if it does not exist
if [ ! -d "$INSTALL_DIR" ]; then
  echo "Creating installation directory at $INSTALL_DIR..."
  mkdir -p "$INSTALL_DIR"
fi

# Copy tool files to the installation directory
SOURCE_DIR="$(dirname "$0")/tool_files"
if [ -d "$SOURCE_DIR" ]; then
  echo "Copying tool files from $SOURCE_DIR to $INSTALL_DIR..."
  cp -r "$SOURCE_DIR/." "$INSTALL_DIR/"
else
  echo "Error: Source directory $SOURCE_DIR does not exist."
  exit 1
fi

# Set executable permissions on all files in the installation directory
echo "Setting executable permissions for files in $INSTALL_DIR..."
chmod -R 755 "$INSTALL_DIR"

# Optionally update the PATH environment variable (user-specific)
PROFILE_FILE="$HOME/.bashrc"
if ! grep -q "$INSTALL_DIR" "$PROFILE_FILE"; then
  echo "Updating PATH in $PROFILE_FILE..."
  echo "export PATH=\$PATH:$INSTALL_DIR" >>"$PROFILE_FILE"
  echo "Please run 'source $PROFILE_FILE' or restart your terminal to update the PATH."
fi

echo "Forensic Tool Two installed successfully."
exit 0
