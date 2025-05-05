#!/bin/bash

# json_to_neo4j.sh - Script to convert JSON to Neo4j Cypher using Python 3.9
# Usage: ./json_to_neo4j.sh [input_json_file]

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Define the path to the sample JSON file (default)
DEFAULT_JSON_FILE="./data/sample_contract.json"
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

# Install dependencies in the correct order to avoid setup issues
echo "Starting dependency installation..."

# First, ensure pip is up-to-date
python -m pip install --upgrade pip setuptools wheel

# Install critical dependencies one by one to avoid conflicts
echo "Installing critical dependencies..."
pip install -q --no-cache-dir "numpy==1.23.5"
pip install -q --no-cache-dir "cython>=0.29.0"
pip install -q --no-cache-dir "scipy>=1.7.0,<1.11.0"
pip install -q --no-cache-dir "torch>=1.10.0,<2.0.0"
pip install -q --no-cache-dir "transformers>=4.15.0,<4.30.0"

# Install remaining dependencies
echo "Installing remaining Python 3.9 specific requirements..."
pip install -q -r requirements-3.9.txt

# Install spaCy model if not already installed
echo "Checking for spaCy model..."
if ! python -c "import spacy; spacy.load('en_core_web_sm')" &> /dev/null; then
  echo "SpaCy model not found. Installing en_core_web_sm model..."
  python -m spacy download en_core_web_sm
fi

# Run the converter script
echo "Running Neo4j converter with Python 3.9 and ContractBERT..."
python json_to_neo4j.py "$JSON_FILE"

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