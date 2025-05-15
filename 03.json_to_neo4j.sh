#!/bin/bash
# Convert JSON to Neo4j Cypher using Python

# ANSI color codes for better output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}JSON to Neo4j Converter${NC}"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Define static paths
JSON_FILE="./data/sample_contract_enhanced.json"
TXT_FILE="./data/sample_contract.txt"

# Get the base name of the file without extension
BASE_NAME=$(basename "$JSON_FILE" .json)
OUTPUT_FILE="${JSON_FILE%.json}.cypher"

# Ensure the virtual environment exists
if [ ! -d ".venv-3.9" ]; then
  echo "Error: Python 3.9 virtual environment '.venv-3.9' not found."
  echo "Please create it first with: python3.9 -m venv .venv-3.9"
  exit 1
fi

# Use Python 3.9 environment
echo "Using Python 3.9 virtual environment..."
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
  echo "Error: transformers library (required for ContractBERT) is not installed."
  echo "Please install it first with: pip install transformers"
  deactivate
  exit 1
fi

# Check if we can initialize transformers pipeline (basic ContractBERT functionality)
if ! python -c "from transformers import pipeline; pipeline('text-classification', model='nlpaueb/legal-bert-base-uncased')" &> /dev/null; then
  echo -e "${RED}❌ Error: Unable to initialize ContractBERT models.${NC}"
  echo -e "Please ensure you have proper internet connection and the models can be downloaded."
  deactivate
  exit 1
fi

# Run the converter script
echo -e "${YELLOW}Converting JSON to Neo4j Cypher script...${NC}"
python src/json_to_neo4j.py --input "$JSON_FILE" --txt "$TXT_FILE" --output "$OUTPUT_FILE"

# Save exit status
EXIT_STATUS=$?

# Deactivate virtual environment
deactivate

# Check the exit status
if [ $EXIT_STATUS -ne 0 ]; then
  echo -e "${RED}❌ Conversion failed. Check the errors above for details.${NC}"
else
  echo -e "${GREEN}✅ Successfully created Neo4j Cypher file!${NC}"
  echo -e "${BLUE}Output file:${NC} $OUTPUT_FILE"
fi
exit $EXIT_STATUS