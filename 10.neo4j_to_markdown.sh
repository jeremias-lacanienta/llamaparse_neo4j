#!/bin/bash
# Neo4j to Markdown Converter
# This script retrieves contract information from Neo4j and generates a Markdown summary

# ANSI color codes for better output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Neo4j to Markdown Converter${NC}"
echo ""

# Static configuration
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="MS110008%5g3"  # Using standard placeholder instead of actual password
DOCUMENT_ID="sample_contract_enhanced"
OUTPUT_FILE="./data/${DOCUMENT_ID}_summary.md"

# Make sure data directory exists
mkdir -p ./data

echo -e "${BLUE}Using static configuration${NC}"
echo ""

# Assume virtual environment already exists
echo -e "${GREEN}Using existing virtual environment...${NC}"
source .venv-3.9/bin/activate

# Install required dependencies from requirements.txt
echo -e "${YELLOW}Installing required dependencies from requirements.txt...${NC}"
pip install -r requirements.txt --quiet
# Make sure Jinja2 is installed
pip install jinja2 --quiet
echo -e "${GREEN}Dependencies installed${NC}"

# Ignore all parameters, use hardcoded values in Python script
echo -e "${YELLOW}Retrieving contract information from Neo4j...${NC}"

# Run the Python script with command line arguments
python3 src/neo4j_to_markdown.py --document-id "$DOCUMENT_ID" --uri "$NEO4J_URI" \
  --user "$NEO4J_USER" --password "$NEO4J_PASSWORD" --output "$OUTPUT_FILE"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}✅ Contract information retrieved and Markdown summary generated!${NC}"
    
        echo -e "${BLUE}Output file:${NC} $OUTPUT_FILE"
    
    # Preview the first few lines
    echo -e "\n${YELLOW}Preview of generated Markdown:${NC}"
    head -n 10 "$OUTPUT_FILE"
    echo -e "..."
else
    echo -e "${RED}❌ Failed to retrieve contract information. Check error messages above.${NC}"
fi

# Deactivate virtual environment
deactivate

exit $exit_code
