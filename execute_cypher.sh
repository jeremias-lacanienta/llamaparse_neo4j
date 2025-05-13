#!/bin/bash
# Neo4j Cypher Script Executor
# This script executes a Cypher script file in Neo4j using cypher-shell

# Configuration variables - customize these
NEO4J_USER="neo4j"
NEO4J_PASSWORD="MS110008%5g3"  # Updated with actual password
CYPHER_FILE="./data/sample_contract_enhanced.cypher"
TEMP_FILE="/tmp/neo4j_cypher_temp.cypher"

# ANSI color codes for better output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=======================================${NC}"
echo -e "${YELLOW}   Neo4j Cypher Script Executor        ${NC}"
echo -e "${YELLOW}=======================================${NC}"
echo ""

# Check if cypher-shell is available
if ! command -v cypher-shell &> /dev/null; then
    # Try to find cypher-shell in Neo4j Desktop installation
    POSSIBLE_PATHS=(
        "~/Library/Application Support/Neo4j Desktop/Application/relate-data/dbmss/dbms-*/bin/cypher-shell"
    )
    
    CYPHER_SHELL=""
    for path_pattern in "${POSSIBLE_PATHS[@]}"; do
        path=$(eval echo "$path_pattern")
        matches=$(ls $path 2>/dev/null)
        if [ ! -z "$matches" ]; then
            # Take the first match
            CYPHER_SHELL=$(echo "$matches" | head -n 1)
            break
        fi
    done
    
    if [ -z "$CYPHER_SHELL" ]; then
        echo -e "${RED}Error: cypher-shell not found in PATH or Neo4j Desktop installation${NC}"
        echo "Please make sure Neo4j is installed correctly or provide the path to cypher-shell manually."
        exit 1
    fi
else
    CYPHER_SHELL="cypher-shell"
fi

# Check if the Cypher file exists
if [ ! -f "$CYPHER_FILE" ]; then
    echo -e "${RED}Error: Cypher file not found: $CYPHER_FILE${NC}"
    exit 1
fi

# Create a temporary file with the BEGIN and COMMIT statements removed
echo -e "${YELLOW}Processing Cypher script...${NC}"
cat "$CYPHER_FILE" | grep -v "^BEGIN$" | grep -v "^COMMIT$" > "$TEMP_FILE"
echo -e "Modified script saved to temporary file: $TEMP_FILE"

# Execute the Cypher script
echo -e "${YELLOW}Importing Cypher script to Neo4j...${NC}"
echo -e "Using: $CYPHER_SHELL"
echo -e "File: $CYPHER_FILE (processed version)"
echo ""

cat "$TEMP_FILE" | $CYPHER_SHELL -u "$NEO4J_USER" -p "$NEO4J_PASSWORD"

# Check the exit status
EXIT_STATUS=$?
if [ $EXIT_STATUS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Import completed successfully${NC}"
    # Clean up the temporary file
    rm "$TEMP_FILE"
    exit 0
else
    echo ""
    echo -e "${RED}✗ Error importing Cypher script${NC}"
    echo -e "The temporary file has been preserved for debugging: $TEMP_FILE"
    exit 1
fi