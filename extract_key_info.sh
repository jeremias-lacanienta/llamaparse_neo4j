#!/bin/bash

# extract_key_info.sh - Script to extract key contract information to Markdown
# Usage: ./extract_key_info.sh [JSON_FILE]

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Define the path to the sample JSON
JSON_FILE=${1:-"./data/sample_contract_enhanced.json"}

# Check if the JSON file exists
if [ ! -f "$JSON_FILE" ]; then
  echo "Error: $JSON_FILE not found."
  echo "Usage: ./extract_key_info.sh [path/to/contract.json]"
  exit 1
fi

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
  echo "Error: transformers library (required for ContractBERT) is not installed."
  echo "Please install it first with: pip install transformers"
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

# Check for the classifier model
if ! python -c "from transformers import pipeline; pipeline('text-classification', model='nlpaueb/legal-bert-base-uncased')" &> /dev/null; then
  echo "Error: Unable to initialize ContractBERT classification model."
  echo "Please ensure you have proper internet connection and the models can be downloaded."
  deactivate
  exit 1
fi

# Run the extraction script
echo "Extracting key information from contract JSON..."
export PYTHONPATH="${PYTHONPATH:-.}:$(pwd)"
python src/extract_key_info.py "$JSON_FILE"

# Save exit status
EXIT_STATUS=$?

# Deactivate virtual environment
deactivate

# Check the exit status
if [ $EXIT_STATUS -ne 0 ]; then
  # Only print error message if the extraction failed
  echo "Extraction failed. Check the logs for details."
else
  # Get the output filename
  OUTPUT_FILE="${JSON_FILE%.*}_key_info.md"
  echo "Successfully extracted key information to: $OUTPUT_FILE"
fi