#!/bin/bash
# Enhance contract JSON with NLP processing

# ANSI color codes for better output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}LlamaParse JSON Converter${NC}"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Load environment variables from .env file
if [ -f .env ]; then
  echo -e "${BLUE}Loading environment variables from .env file...${NC}"
  export $(grep -v '^#' .env | xargs)
fi

# Define paths with command-line arguments support
JSON_FILE="${1:-./data/sample_contract.json}"
TXT_FILE="${2:-./data/sample_contract.txt}"
OUTPUT_FILE="${3:-${JSON_FILE%.*}_enhanced.json}"

# Display the paths we're using
echo -e "${BLUE}Input JSON:${NC} $JSON_FILE"
echo -e "${BLUE}Input TXT:${NC} $TXT_FILE"
echo -e "${BLUE}Output:${NC} $OUTPUT_FILE"

# Ensure the Python 3.9 virtual environment exists
if [ ! -d ".venv-3.9" ]; then
  echo "Error: Virtual environment '.venv-3.9' not found."
  echo "Please create it first with: python3.9 -m venv .venv-3.9"
  exit 1
fi

# Activate the Python 3.9 virtual environment
echo "Activating Python 3.9 virtual environment..."
source .venv-3.9/bin/activate

# Check for spaCy and ContractBERT dependencies
echo "Checking for required dependencies..."

# Check for spaCy
if ! python -c "import spacy" &> /dev/null; then
  echo "Error: spaCy is not installed in the virtual environment."
  echo "Please install it first with: pip install spacy"
  deactivate
  exit 1
fi

# Check for spaCy model
if ! python -c "import spacy; spacy.load('en_core_web_lg')" &> /dev/null; then
  echo "Error: SpaCy model 'en_core_web_lg' not found."
  echo "Please install it with: python -m spacy download en_core_web_lg"
  deactivate
  exit 1
fi

# Check for transformers (ContractBERT dependency)
if ! python -c "import transformers" &> /dev/null; then
  echo -e "${RED}❌ Error: transformers library (required for ContractBERT) is not installed.${NC}"
  echo -e "Please install it first with: pip install transformers"
  deactivate
  exit 1
fi

# Check if we can initialize transformers pipeline (basic ContractBERT functionality)
if ! python -c "from transformers import pipeline; pipeline('token-classification', model='nlpaueb/legal-bert-base-uncased', aggregation_strategy='simple')" &> /dev/null; then
  echo "Error: Unable to initialize ContractBERT NER model."
  echo "Please ensure you have proper internet connection and the models can be downloaded."
  deactivate
  exit 1
fi

# Run the converter script
echo -e "${YELLOW}Enhancing contract JSON with NLP analysis...${NC}"
python src/llamaparse_converter.py --json "$JSON_FILE" --txt "$TXT_FILE" --output "$OUTPUT_FILE"

# Save exit status
EXIT_STATUS=$?

# Deactivate virtual environment
# deactivate

# Check the exit status
if [ $EXIT_STATUS -ne 0 ]; then
  # Only print error message if the conversion failed
  echo -e "${RED}❌ Enhancement failed. Check the logs for details.${NC}"
else
  # Get the output filename
  OUTPUT_FILE="${JSON_FILE%.*}_enhanced.json"
  echo -e "${GREEN}✅ Successfully enhanced contract data!${NC}"
  echo -e "${BLUE}Output file:${NC} $OUTPUT_FILE"
fi
exit $EXIT_STATUS