# LlamaParse to Neo4j Converter

A comprehensive toolkit for converting PDF contracts into structured graph databases using LlamaParse, SpaCy, and Neo4j.

## Overview

This project provides a pipeline for:
1. Converting PDF contracts to JSON, Markdown, and TXT formats
2. Enhancing contract structure with NLP (Natural Language Processing)
3. Converting contract data to Neo4j graph database format
4. Executing Cypher queries to populate a Neo4j database
5. Extracting key information from contracts
6. Generating Markdown summaries from Neo4j data

## New Feature: TXT Fallback Strategy

The toolkit now includes a TXT fallback strategy that uses regex patterns on TXT files when JSON structure is inadequate. This improves extraction reliability when LlamaParse produces inconsistent JSON structures, particularly for complex layouts or bounding boxes.

### Benefits of the TXT Fallback Strategy:
- More reliable extraction of contract articles and sections
- Improved processing of documents with complex layouts
- Hybrid approach that combines JSON structure with TXT when needed
- Better handling of cases where LlamaParse JSON has issues

## Usage

### Step 1: Convert PDF to Various Formats

```bash
./01.convert_pdf.sh [input_pdf_file]
```

This script converts a PDF file to multiple formats:
- JSON: For structured data extraction
- Markdown: For human-readable content
- TXT: For fallback extraction with regex patterns

### Step 2: Enhance Contract JSON with NLP

```bash
./02.llamaparse_converter.sh [input_json_file] [input_txt_file]
```

Enhances contract JSON data with NLP analysis using SpaCy and ContractBERT.
Now with TXT fallback option for improved extraction when JSON structure has issues.

### Step 3: Convert JSON to Neo4j Cypher

```bash
./03.json_to_neo4j.sh [input_json_file] [input_txt_file]
```

Processes enhanced JSON (with TXT fallback) and generates Neo4j Cypher statements.

### Step 4: Execute Cypher in Neo4j

```bash
./04.execute_cypher.sh [cypher_file]
```

Executes the generated Cypher statements against a Neo4j database.

### Step 5: Extract Key Information

```bash
./10.extract_key_info.sh [json_file] [txt_file]
```

Extracts key information from the contract and outputs a summary.

### Step 6: Generate Markdown from Neo4j

```bash
./10.neo4j_to_markdown.sh [output_file]
```

Generates a Markdown summary from Neo4j database content.

## Requirements

- Python 3.9+ (recommended for optimal compatibility)
- Neo4j database
- LlamaParse API key
- SpaCy with en_core_web_lg model
- ContractBERT NLP models

## Setup

1. Create a Python virtual environment:
   ```bash
   python3.9 -m venv .venv-3.9
   ```

2. Install dependencies:
   ```bash
   source .venv-3.9/bin/activate
   pip install -r requirements-3.9.txt
   ```

3. Download SpaCy model:
   ```bash
   python -m spacy download en_core_web_lg
   ```

4. Create a `.env` file with your API keys:
   ```
   LLAMA_CLOUD_API_KEY=your_llamaparse_api_key
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
