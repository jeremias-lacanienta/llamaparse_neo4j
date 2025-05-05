#!/bin/bash

# run_converter.sh - Script to execute the LlamaParse converter
# Usage: ./run_converter.sh

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Define the path to the sample PDF
PDF_FILE="./data/sample_contract.pdf"

# Check if the sample PDF exists
if [ ! -f "$PDF_FILE" ]; then
  echo "Error: $PDF_FILE not found."
  echo "Please ensure the sample PDF file exists in the data directory."
  exit 1
fi

# Ensure the virtual environment exists
if [ ! -d ".venv" ]; then
  echo "Error: Virtual environment '.venv' not found."
  echo "Please create it first with: python -m venv .venv"
  exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check for and install required Python packages without verbose output
echo "Installing Python requirements..."
pip install -q -r requirements.txt

# Run the converter script
echo "Running LlamaParse converter to generate all formats..."
python llamaparse_converter.py "$PDF_FILE"

# Save exit status
EXIT_STATUS=$?

# Deactivate virtual environment
# deactivate

# Check the exit status
if [ $EXIT_STATUS -ne 0 ]; then
  # Only print error message if the conversion failed
  echo "Conversion failed. Check the logs for details."
else
  echo "Successfully converted PDF to all formats using LlamaParse"
fi