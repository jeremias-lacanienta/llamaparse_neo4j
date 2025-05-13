#!/bin/bash

# backup_and_clean.sh - Script to backup important files
# Usage: ./backup_and_clean.sh

# Set timestamp for backup files
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backup_$TIMESTAMP"
BACKUP_ZIP="llamaparse_neo4j_backup_$TIMESTAMP.zip"

echo "Starting backup process..."

# Create backup directory
mkdir -p "$BACKUP_DIR"
echo "Created backup directory: $BACKUP_DIR"

# Backup shell scripts
echo "Backing up shell scripts..."
cp *.sh "$BACKUP_DIR/"

# Backup Python source files (excluding __pycache__)
echo "Backing up Python source files..."
mkdir -p "$BACKUP_DIR/src"
cp -r src/*.py "$BACKUP_DIR/src/"
mkdir -p "$BACKUP_DIR/src/extract"
cp -r src/extract/*.py "$BACKUP_DIR/src/extract/"

# Backup templates
echo "Backing up templates..."
mkdir -p "$BACKUP_DIR/templates"
cp -r templates/* "$BACKUP_DIR/templates/"

# Backup requirements files
echo "Backing up requirements files..."
cp requirements*.txt "$BACKUP_DIR/" 2>/dev/null

# Backup README
echo "Backing up README.md..."
cp README.md "$BACKUP_DIR/"

# Backup sample PDF file
echo "Backing up sample PDF file..."
cp sample_contract.pdf "$BACKUP_DIR/"

# Backup data folder
echo "Backing up data folder..."
mkdir -p "$BACKUP_DIR/data"
cp -r data/* "$BACKUP_DIR/data/"

# Create zip archive of shell scripts, templates, Python files, and data
# Exclude __pycache__ directories and previous backups
echo "Creating zip archive of important files..."
find . -maxdepth 1 \( -name "*.sh" -o -name "src" -o -name "templates" -o -name "requirements*.txt" -o -name "README.md" -o -name "sample_contract.pdf" -o -name "data" \) | grep -v "llamaparse_neo4j_backup_" | zip -r "$BACKUP_ZIP" -x "**/__pycache__/*" -@ 2>/dev/null

# Remove backup directory after creating zip
echo "Removing temporary backup directory..."
rm -rf "$BACKUP_DIR"

# Clean up logs directory
echo "Cleaning logs directory..."
rm -f logs/*

# Clean up data directory - delete everything without exceptions
echo "Cleaning data directory..."
rm -rf data/*

echo "Backup process completed."
echo "Backup zip archive: $BACKUP_ZIP"
echo ""
echo "Summary of actions:"
echo "1. Created zip archive: $BACKUP_ZIP (excluding __pycache__ directories)"
echo "2. Backed up all files from data/ directory"
echo "3. Deleted ALL files from data/ directory"
echo "4. Deleted all files from logs/ directory"