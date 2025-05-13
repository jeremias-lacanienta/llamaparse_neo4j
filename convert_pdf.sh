#!/bin/bash

# convert_pdf.sh - Script to convert PDF files to JSON, Markdown, and text formats using LlamaParse
# Usage: ./convert_pdf.sh [input_pdf_file]

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Set default values
PDF_FILE=${1:-"./sample_contract.pdf"}
OUTPUT_DIR="./data"
PDF_BASENAME=$(basename "$PDF_FILE" .pdf)
OUTPUT_BASE="${OUTPUT_DIR}/${PDF_BASENAME}"

# Load environment variables from .env file
if [ -f .env ]; then
  echo "Loading environment variables from .env file..."
  export $(grep -v '^#' .env | xargs)
fi

# Check if LLAMA_CLOUD_API_KEY is set
if [ -z "${LLAMA_CLOUD_API_KEY}" ]; then
  echo "Error: LLAMA_CLOUD_API_KEY environment variable not set."
  echo "Please set it in your .env file or export it directly."
  exit 1
fi

# Check if the PDF file exists
if [ ! -f "$PDF_FILE" ]; then
  echo "Error: $PDF_FILE not found."
  echo "Please provide a valid PDF file path."
  exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Ensure the Python virtual environment exists
if [ ! -d ".venv" ]; then
  echo "Error: Virtual environment '.venv' not found."
  echo "Please create it first with: python -m venv .venv"
  exit 1
fi

# Activate the Python virtual environment
echo "Activating Python virtual environment..."
source .venv/bin/activate

# Check if llama-parse is installed
if ! command -v llama-parse &> /dev/null; then
  # Install/upgrade llama-index
  echo "Updating llama-index package..."
  pip uninstall -y llama-index  # run this if upgrading from v0.9.x or older
  pip install -U llama-index --upgrade --no-cache-dir --force-reinstall
  echo "Error: llama-parse is not installed in the virtual environment."
  echo "Installing llama-parse..."
  pip install llama-parse
fi

# Convert to JSON format
echo "Converting $PDF_FILE to JSON format..."
llama-parse "$PDF_FILE" --output-raw-json --output-file "${OUTPUT_BASE}.json"
JSON_STATUS=$?

# Convert to Markdown format
echo "Converting $PDF_FILE to Markdown format..."
llama-parse "$PDF_FILE" --result-type markdown --output-file "${OUTPUT_BASE}.md"
MD_STATUS=$?

# Convert to text format
echo "Converting $PDF_FILE to text format..."
llama-parse "$PDF_FILE" --result-type text --output-file "${OUTPUT_BASE}.txt"
TXT_STATUS=$?

# Deactivate virtual environment
deactivate

# Check the exit status
if [ $JSON_STATUS -ne 0 ] || [ $MD_STATUS -ne 0 ] || [ $TXT_STATUS -ne 0 ]; then
  echo "Error: One or more conversions failed. Check the output for details."
  exit 1
else
  echo "Conversion completed successfully!"
  echo "Output files:"
  echo "  JSON: ${OUTPUT_BASE}.json"
  echo "  Markdown: ${OUTPUT_BASE}.md"
  echo "  Text: ${OUTPUT_BASE}.txt"
fi