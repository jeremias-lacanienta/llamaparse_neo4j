# Neo4j to Markdown Documentation

This document explains how to use the Neo4j to Markdown converter to generate comprehensive contract summaries from data stored in Neo4j.

## Overview

The `neo4j_to_markdown.py` script retrieves contract information from a Neo4j database and generates a Markdown summary using the same template as the JSON-based extractor. This allows you to view contract information in a well-formatted, easily readable format after it has been stored in Neo4j.

## Requirements

- Neo4j database with contract data (imported using the `extract_to_neo4j.sh` script)
- Python 3.9+ with requirements from `requirements.txt`
- Access credentials for the Neo4j database

## Usage

### Using the Shell Script

The easiest way to use the converter is with the provided shell script:

```bash
./neo4j_to_markdown.sh <document_id> [options]
```

#### Arguments:

- `document_id` - The document ID of the contract in the Neo4j database

#### Options:

- `-o, --output FILE` - Path to output Markdown file (default: `<document_id>_summary.md`)
- `-u, --uri URI` - Neo4j server URI (default: bolt://localhost:7687)
- `-n, --username USER` - Neo4j username (default: neo4j)
- `-p, --password PASS` - Neo4j password (will prompt if not provided)
- `-h, --help` - Show help message

#### Example:

```bash
./neo4j_to_markdown.sh sample_contract -o contract_summary.md -u bolt://localhost:7687 -n neo4j
```

### Using the Python Script Directly

You can also run the Python script directly:

```bash
python src/neo4j_to_markdown.py <document_id> [options]
```

#### Arguments:

- `document_id` - The document ID of the contract in the Neo4j database

#### Options:

- `-o, --output` - Path to output Markdown file
- `-u, --uri` - Neo4j server URI (default: bolt://localhost:7687)
- `-n, --username` - Neo4j username (default: neo4j)
- `-p, --password` - Neo4j password (will prompt if not provided)

#### Example:

```bash
python src/neo4j_to_markdown.py sample_contract -o contract_summary.md -u bolt://localhost:7687 -n neo4j
```

## How It Works

1. The script connects to the Neo4j database using the provided credentials
2. It retrieves all contract information using Cypher queries based on the document ID
3. The data is organized into a structure matching the one from the JSON extractor
4. A Markdown file is generated using the Jinja2 template from the templates directory
5. The output is saved to the specified file path

## Common Issues and Solutions

### Connection Issues

If you're having trouble connecting to Neo4j, check:
- Neo4j server is running
- URI, username, and password are correct
- Network connectivity to the Neo4j server
- Neo4j APOC plugin is installed if using some complex queries

### Missing Data

If some data is missing from the output:
- Ensure the contract was properly imported with `extract_to_neo4j.sh`
- Check if the document ID exactly matches the one in Neo4j
- Run a direct Cypher query in the Neo4j browser to verify the data exists

### Template Issues

If the Markdown formatting is incorrect:
- Ensure the template file exists in the templates directory
- Check for any syntax errors in the Jinja2 template
