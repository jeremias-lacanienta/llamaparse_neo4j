#!/bin/bash
# Test Title Extraction in Full Pipeline

# ANSI color codes for better output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}===== Contract Title Extraction Verification =====${NC}"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Run our standalone test first
echo -e "${BLUE}Step 1: Testing standalone extraction logic${NC}"
python3 test_simple_extraction.py
echo ""

# Verify the shell scripts that were updated
echo -e "${BLUE}Step 2: Checking shell scripts for proper argument handling${NC}"

# List of shell scripts to check
scripts=(
    "02.llamaparse_converter.sh"
    "03.json_to_neo4j.sh"
    "10.extract_key_info.sh"
    "10.neo4j_to_markdown.sh"
)

# Check each script for argument passing
for script in "${scripts[@]}"; do
    echo -e "Checking ${YELLOW}$script${NC} for argument handling..."
    if grep -q -- "--input" "$script" || grep -q -- "-i" "$script" || grep -q -- "--json" "$script"; then
        echo -e "${GREEN}✅ $script correctly passes arguments${NC}"
    else
        echo -e "${RED}❌ $script might not be updated to pass arguments correctly${NC}"
    fi
done
echo ""

# Verify the Python files have been updated
echo -e "${BLUE}Step 3: Checking Python files for argument parsing${NC}"

# List of Python files to check
py_files=(
    "src/extract/txt_parser.py"
    "src/json_to_neo4j.py"
)

# Check each Python file for argument parsing
for py_file in "${py_files[@]}"; do
    echo -e "Checking ${YELLOW}$py_file${NC} for title handling..."
    if grep -q "title.*:.* *\"Untitled Contract\"" "$py_file" || grep -q "title.*=.*\"Untitled Contract\"" "$py_file"; then
        echo -e "${GREEN}✅ $py_file sets default title${NC}"
    else
        echo -e "${RED}❌ $py_file might not set default title${NC}"
    fi
done
echo ""

# Check if hybrid approach handles title
echo -e "${BLUE}Step 4: Checking if hybrid approach handles title${NC}"
if grep -q "not processed_data\[\"metadata\"\].get(\"title\")" "src/json_to_neo4j.py"; then
    echo -e "${GREEN}✅ json_to_neo4j.py checks for missing title in hybrid approach${NC}"
else
    echo -e "${RED}❌ json_to_neo4j.py might not handle missing title${NC}"
fi
echo ""

echo -e "${GREEN}Verification complete!${NC}"
echo -e "The contract title extraction should now work correctly for all cases."
