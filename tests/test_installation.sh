#!/bin/bash
# ------------------------------------------------------------------
# Automated Installation Test Script for Forensic Tools Installer
# ------------------------------------------------------------------
# This script reads the configuration from the installer and
# executes the installation scripts for each tool. It logs the
# output to a log file for review.
#
# Prerequisites:
# - Ensure 'jq' is installed on your system for JSON parsing.
# - Run as root if the installation scripts require administrative privileges.
# ------------------------------------------------------------------

# Define paths
CONFIG_FILE="../installer/config.json"
LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/test_installation.log"

# Create logs directory if it doesn't exist
mkdir -p "${LOG_DIR}"

# Initialize log file
echo "=== Automated Installation Test Log ===" >"${LOG_FILE}"
echo "Start Time: $(date)" >>"${LOG_FILE}"
echo "----------------------------------------" >>"${LOG_FILE}"

# Verify that the configuration file exists
if [ ! -f "${CONFIG_FILE}" ]; then
  echo "Error: Config file not found at ${CONFIG_FILE}" | tee -a "${LOG_FILE}"
  exit 1
fi

# Extract tool keys from the config using jq
TOOL_KEYS=$(jq -r '.tools | keys[]' "${CONFIG_FILE}")

# Loop through each tool defined in the config
for tool in ${TOOL_KEYS}; do
  TOOL_NAME=$(jq -r ".tools[\"${tool}\"].name" "${CONFIG_FILE}")
  SCRIPT_REL_PATH=$(jq -r ".tools[\"${tool}\"].script" "${CONFIG_FILE}")
  VALIDATION_CMD=$(jq -r ".tools[\"${tool}\"].validation_cmd" "${CONFIG_FILE}")

  echo "Testing installation for ${TOOL_NAME}..." | tee -a "${LOG_FILE}"

  # Determine the absolute path to the installation script
  # The script is located relative to the tool's directory
  TOOL_DIR=$(dirname "${CONFIG_FILE}")/../tools/${tool}
  SCRIPT_NAME=$(basename "${SCRIPT_REL_PATH}")
  SCRIPT_PATH="${TOOL_DIR}/${SCRIPT_NAME}"

  if [ ! -d "${TOOL_DIR}" ]; then
    echo "Error: Tool directory not found: ${TOOL_DIR}" | tee -a "${LOG_FILE}"
    continue
  fi

  if [ ! -f "${SCRIPT_PATH}" ]; then
    echo "Error: Installation script not found: ${SCRIPT_PATH}" | tee -a "${LOG_FILE}"
    continue
  fi

  # Warn if not running as root
  if [ "$EUID" -ne 0 ]; then
    echo "Warning: Not running as root. Some installation scripts may require elevated privileges." | tee -a "${LOG_FILE}"
  fi

  # Execute the installation script and log output
  echo "Executing installation script: ${SCRIPT_PATH}" | tee -a "${LOG_FILE}"
  bash "${SCRIPT_PATH}" >>"${LOG_FILE}" 2>&1
  INSTALL_EXIT_CODE=$?

  if [ ${INSTALL_EXIT_CODE} -eq 0 ]; then
    echo "${TOOL_NAME} installation script executed successfully." | tee -a "${LOG_FILE}"
    # Validate the installation by running the validation command
    echo "Running validation command: ${VALIDATION_CMD}" | tee -a "${LOG_FILE}"
    VALID_OUTPUT=$(${VALIDATION_CMD} 2>&1)
    if echo "${VALID_OUTPUT}" | grep -qi "version"; then
      echo "Validation passed for ${TOOL_NAME}." | tee -a "${LOG_FILE}"
    else
      echo "Validation failed for ${TOOL_NAME}. Output:" | tee -a "${LOG_FILE}"
      echo "${VALID_OUTPUT}" | tee -a "${LOG_FILE}"
    fi
  else
    echo "Error: ${TOOL_NAME} installation script failed with exit code ${INSTALL_EXIT_CODE}." | tee -a "${LOG_FILE}"
  fi

  echo "----------------------------------------" >>"${LOG_FILE}"
done

echo "Test completed at: $(date)" >>"${LOG_FILE}"
echo "Log file saved at: ${LOG_FILE}"
