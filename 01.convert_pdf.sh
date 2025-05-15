#!/bin/bash
# Convert PDF to various formats using LlamaParse

# ANSI color codes for better output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}PDF Converter (LlamaParse)${NC}"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Set fixed values
PDF_FILE="./sample_contract.pdf"
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
echo -e "${YELLOW}Converting $PDF_FILE to JSON format...${NC}"
llama-parse "$PDF_FILE" --output-raw-json --output-file "${OUTPUT_BASE}.json"
JSON_STATUS=$?

# Convert to Markdown format
echo -e "${YELLOW}Converting $PDF_FILE to Markdown format...${NC}"
llama-parse "$PDF_FILE" --result-type markdown --output-file "${OUTPUT_BASE}.md"
MD_STATUS=$?

# Convert to text format
echo -e "${YELLOW}Converting $PDF_FILE to text format...${NC}"
llama-parse "$PDF_FILE" --result-type text --output-file "${OUTPUT_BASE}.txt"
TXT_STATUS=$?

# Deactivate virtual environment
deactivate

# Check the exit status
if [ $JSON_STATUS -ne 0 ] || [ $MD_STATUS -ne 0 ] || [ $TXT_STATUS -ne 0 ]; then
  echo -e "${RED}❌ Error: One or more conversions failed. Check the output for details.${NC}"
  exit 1
else
  echo -e "${GREEN}✅ All conversions completed successfully.${NC}"
  echo -e "${BLUE}Output files:${NC}"
  echo -e "  JSON: ${OUTPUT_BASE}.json"
  echo -e "  Markdown: ${OUTPUT_BASE}.md"
  echo -e "  Text: ${OUTPUT_BASE}.txt"
  exit 0
fi