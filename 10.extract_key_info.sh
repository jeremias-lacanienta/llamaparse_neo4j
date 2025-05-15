#!/bin/bash
# Extract key contract information to Markdown

# ANSI color codes for better output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Contract Key Information Extractor${NC}"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Define static paths
JSON_FILE="./data/sample_contract_enhanced.json"
OUTPUT_FILE="${JSON_FILE%.*}_key_info.md"

# Ensure the Python 3.9 virtual environment exists
if [ ! -d ".venv-3.9" ]; then
  echo -e "${RED}❌ Error: Virtual environment '.venv-3.9' not found.${NC}"
  echo -e "Please create it first with: python3.9 -m venv .venv-3.9"
  exit 1
fi

# Activate the Python 3.9 virtual environment
echo -e "${YELLOW}Activating Python 3.9 virtual environment...${NC}"
source .venv-3.9/bin/activate

# Check for spaCy and ContractBERT dependencies
echo -e "${YELLOW}Checking for required dependencies...${NC}"

# Check for spaCy
if ! python -c "import spacy" &> /dev/null; then
  echo -e "${RED}❌ Error: spaCy is not installed in the virtual environment.${NC}"
  echo -e "Please install it first with: pip install spacy"
  deactivate
  exit 1
fi

# Check for spaCy model
if ! python -c "import spacy; spacy.load('en_core_web_lg')" &> /dev/null; then
  echo -e "${RED}❌ Error: SpaCy model 'en_core_web_lg' not found.${NC}"
  echo -e "Please install it with: python -m spacy download en_core_web_lg"
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
  echo -e "${RED}❌ Error: Unable to initialize ContractBERT NER model.${NC}"
  echo -e "Please ensure you have proper internet connection and the models can be downloaded."
  deactivate
  exit 1
fi

# Check for the classifier model
if ! python -c "from transformers import pipeline; pipeline('text-classification', model='nlpaueb/legal-bert-base-uncased')" &> /dev/null; then
  echo -e "${RED}❌ Error: Unable to initialize ContractBERT classification model.${NC}"
  echo -e "Please ensure you have proper internet connection and the models can be downloaded."
  deactivate
  exit 1
fi

# Run the extraction script
echo -e "${YELLOW}Extracting key information from contract JSON...${NC}"
export PYTHONPATH="${PYTHONPATH:-.}:$(pwd)"
python src/extract_key_info.py --input "$JSON_FILE" --output "$OUTPUT_FILE"

# Save exit status
EXIT_STATUS=$?

# Deactivate virtual environment
deactivate

# Check the exit status
if [ $EXIT_STATUS -ne 0 ]; then
  # Only print error message if the extraction failed
  echo -e "${RED}❌ Extraction failed. Check the logs for details.${NC}"
else
  # Get the output filename
  OUTPUT_FILE="${JSON_FILE%.*}_key_info.md"
  echo -e "${GREEN}✅ Successfully extracted key information!${NC}"
  echo -e "${BLUE}Output file:${NC} $OUTPUT_FILE"
fi
exit $EXIT_STATUS