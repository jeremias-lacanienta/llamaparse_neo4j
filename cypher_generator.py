#!/usr/bin/env python3
"""
Cypher Generator for Contract Analysis

This module handles the generation of Neo4j Cypher commands for importing
contract data into a graph database. It converts the structured contract data
into a graph representation with nodes for contracts, parties, articles, sections, etc.
"""

import re
import json
import sys
import os
from typing import Dict, List, Any
from datetime import datetime


def generate_neo4j_cypher(contract_metadata: Dict[str, Any], 
                         articles: List[Dict[str, Any]], 
                         parties: List[Dict[str, Any]], 
                         document_name: str, 
                         document_id: str, 
                         timestamp: str) -> List[str]:
    """Generate Cypher commands for Neo4j database.
    
    Args:
        contract_metadata: Dictionary with contract metadata (title, date, type)
        articles: List of article dictionaries with their sections
        parties: List of party dictionaries with their details
        document_name: Name of the source document
        document_id: Identifier of the source document
        timestamp: Timestamp of the import
        
    Returns:
        List of Cypher commands ready to be executed in Neo4j
    """
    cypher_commands = []
    
    # Create Contract node
    contract_cypher = (
        f"CREATE (c:Contract {{title: '{contract_metadata['title']}', "
        f"effectiveDate: '{contract_metadata['effective_date']}', "
        f"documentType: '{contract_metadata['document_type']}', "
        f"sourceDocument: '{document_name}', "
        f"documentId: '{document_id}', "
        f"importTimestamp: '{timestamp}' }})"
    )
    cypher_commands.append(contract_cypher)
    
    # Create Party nodes and relationships to Contract
    for idx, party in enumerate(parties):
        party_id = f"p{idx}"
        party_cypher = (
            f"CREATE ({party_id}:Party {{name: '{party['name']}', "
            f"type: '{party['type']}', "
            f"sourceDocument: '{document_name}', "
            f"documentId: '{document_id}' }})"
        )
        cypher_commands.append(party_cypher)
        
        # Create relationship between Party and Contract
        rel_cypher = f"CREATE ({party_id})-[:PARTY_TO]->(c)"
        cypher_commands.append(rel_cypher)
        
        # Create Signatory nodes
        for sig_idx, signatory in enumerate(party.get("signatories", [])):
            sig_id = f"s{idx}_{sig_idx}"
            sig_cypher = (
                f"CREATE ({sig_id}:Person {{name: '{signatory['name']}', "
                f"title: '{signatory['title']}', "
                f"sourceDocument: '{document_name}', "
                f"documentId: '{document_id}' }})"
            )
            cypher_commands.append(sig_cypher)
            
            # Create relationship between Signatory and Party
            sig_rel_cypher = f"CREATE ({sig_id})-[:REPRESENTS]->({party_id})"
            cypher_commands.append(sig_rel_cypher)
    
    # Create Article nodes and relationships to Contract
    for idx, article in enumerate(articles):
        article_id = f"a{idx}"
        article_cypher = (
            f"CREATE ({article_id}:Article {{number: '{article['number']}', "
            f"title: '{article['title']}', "
            f"sourceDocument: '{document_name}', "
            f"documentId: '{document_id}' }})"
        )
        cypher_commands.append(article_cypher)
        
        # Create relationship between Article and Contract
        art_rel_cypher = f"CREATE (c)-[:CONTAINS]->({article_id})"
        cypher_commands.append(art_rel_cypher)
        
        # Create Section nodes and relationships to Article
        for sec_idx, section in enumerate(article.get("sections", [])):
            sec_id = f"s{idx}_{sec_idx}"
            # Escape single quotes in content
            content = section.get("content", "").replace("'", "\\'")
            # Truncate content if too long
            if len(content) > 500:
                content = content[:497] + "..."
                
            sec_cypher = (
                f"CREATE ({sec_id}:Section {{number: '{section['number']}', "
                f"title: '{section['title']}', "
                f"content: '{content}', "
                f"sourceDocument: '{document_name}', "
                f"documentId: '{document_id}' }})"
            )
            cypher_commands.append(sec_cypher)
            
            # Create relationship between Section and Article
            sec_rel_cypher = f"CREATE ({article_id})-[:HAS_SECTION]->({sec_id})"
            cypher_commands.append(sec_rel_cypher)
    
    return cypher_commands


def write_cypher_to_file(cypher_commands: List[str], output_file: str) -> None:
    """Write Cypher commands to an output file.
    
    Args:
        cypher_commands: List of Cypher commands to write
        output_file: Path to the output file
    """
    try:
        with open(output_file, 'w') as f:
            f.write("// Neo4j Cypher Import Script\n")
            f.write(f"// Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("// This script will create a graph representation of the contract\n\n")
            
            # Add a transaction wrapper
            f.write("BEGIN\n\n")
            
            # First, add a statement to clear existing data (commented out by default)
            f.write("// Uncomment to clear existing data before import\n")
            f.write("// MATCH (n) DETACH DELETE n;\n\n")
            
            # Write each Cypher command
            for cmd in cypher_commands:
                f.write(f"{cmd};\n")
            
            f.write("\nCOMMIT\n")
        
        print(f"Successfully generated Neo4j Cypher commands in {output_file}")
        
    except Exception as e:
        print(f"Error writing Cypher file: {e}")
        raise


def process_json_file(input_file: str, output_file: str, 
                     extract_contract_metadata_func,
                     extract_articles_func,
                     extract_parties_func) -> None:
    """Process the input JSON file and generate Neo4j Cypher commands.
    
    Args:
        input_file: Path to the input JSON file
        output_file: Path to the output Cypher file
        extract_contract_metadata_func: Function to extract contract metadata
        extract_articles_func: Function to extract articles and sections
        extract_parties_func: Function to extract party information
    """
    try:
        # Get the filename for document tracking
        document_name = os.path.basename(input_file)
        document_id = os.path.splitext(document_name)[0]  # Remove extension
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Extract metadata, articles, and parties using the provided functions
        contract_metadata = extract_contract_metadata_func(data)
        articles = extract_articles_func(data)
        parties = extract_parties_func(data)
        
        # Generate Cypher commands
        cypher_commands = generate_neo4j_cypher(contract_metadata, articles, parties, document_name, document_id, timestamp)
        
        # Write Cypher commands to output file
        write_cypher_to_file(cypher_commands, output_file)
        
        print(f"Successfully generated Neo4j Cypher commands in {output_file}")
        
    except Exception as e:
        print(f"Error processing JSON file: {e}", file=sys.stderr)
        raise