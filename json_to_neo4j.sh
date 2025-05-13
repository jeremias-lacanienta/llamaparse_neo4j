#!/bin/bash

# json_to_neo4j.sh - Script to convert JSON to Neo4j Cypher using Python 3.9
# Usage: ./json_to_neo4j.sh [input_json_file]

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Define the path to the sample JSON file (default)
DEFAULT_JSON_FILE="./data/sample_contract_enhanced.json"
JSON_FILE=${1:-$DEFAULT_JSON_FILE}

# Check if the JSON file exists
if [ ! -f "$JSON_FILE" ]; then
  echo "Error: $JSON_FILE not found."
  echo "Please provide a valid JSON file path or ensure the sample file exists."
  exit 1
fi

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
  echo "Error: Unable to initialize ContractBERT models."
  echo "Please ensure you have proper internet connection and the models can be downloaded."
  deactivate
  exit 1
fi

# Run the converter script
echo "Running Neo4j converter with Python 3.9, ContractBERT, and SpaCy large model..."
python src/json_to_neo4j.py "$JSON_FILE"

# Save exit status
EXIT_STATUS=$?

# Deactivate virtual environment
deactivate

# Check the exit status
if [ $EXIT_STATUS -ne 0 ]; then
  echo "Conversion failed. Check the errors above for details."
  exit 1
else
  echo "Successfully created Neo4j Cypher file: $OUTPUT_FILE"
fi