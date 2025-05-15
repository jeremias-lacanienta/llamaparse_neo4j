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
                     metadata: Dict[str, Any],
                     articles: List[Dict[str, Any]],
                     parties: List[Dict[str, Any]],
                     key_provisions: List[Dict[str, Any]] = None,
                     financials: List[Dict[str, Any]] = None,
                     dates: List[Dict[str, Any]] = None,
                     terms: Dict[str, List[str]] = None,
                     entities: Dict[str, List[str]] = None) -> None:
    """Process the input JSON file and generate Neo4j Cypher commands.
    
    Args:
        input_file: Path to the input JSON file
        output_file: Path to the output Cypher file
        metadata: Contract metadata (title, date, type)
        articles: List of articles with their sections
        parties: List of parties with their details
        key_provisions: List of key provisions extracted from the contract
        financials: List of financial mentions with context
        dates: List of date mentions with context
        terms: Dictionary of key legal terms with context examples
        entities: Dictionary of named entities by entity type
    """
    try:
        # Get the filename for document tracking
        document_name = os.path.basename(input_file)
        document_id = os.path.splitext(document_name)[0]  # Remove extension
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate basic Cypher commands
        cypher_commands = generate_neo4j_cypher(
            metadata, articles, parties, document_name, document_id, timestamp
        )
        
        # Generate additional Cypher commands for the enhanced data
        if key_provisions:
            cypher_commands.extend(
                generate_key_provisions_cypher(key_provisions, document_name, document_id)
            )
            
        if financials:
            cypher_commands.extend(
                generate_financials_cypher(financials, document_name, document_id)
            )
            
        if dates:
            cypher_commands.extend(
                generate_dates_cypher(dates, document_name, document_id)
            )
            
        if terms:
            cypher_commands.extend(
                generate_terms_cypher(terms, document_name, document_id)
            )
            
        if entities:
            cypher_commands.extend(
                generate_entities_cypher(entities, document_name, document_id)
            )
        
        # Write Cypher commands to output file
        write_cypher_to_file(cypher_commands, output_file)
        
        print(f"Successfully generated Neo4j Cypher commands in {output_file}")
        
    except Exception as e:
        print(f"Error processing JSON file: {e}", file=sys.stderr)
        raise


def generate_key_provisions_cypher(key_provisions: List[Dict[str, Any]], 
                                 document_name: str, 
                                 document_id: str) -> List[str]:
    """Generate Cypher commands for key provisions.
    
    Args:
        key_provisions: List of key provisions
        document_name: Name of the source document
        document_id: Identifier of the source document
        
    Returns:
        List of Cypher commands for key provisions
    """
    cypher_commands = []
    
    # Find the contract node reference
    contract_ref = "(c:Contract {documentId: '" + document_id + "'})"
    
    for idx, provision in enumerate(key_provisions):
        # Clean text for Cypher query
        number = provision.get("number", "").replace("'", "\\'")
        title = provision.get("title", "").replace("'", "\\'")
        summary = provision.get("summary", "").replace("'", "\\'")
        
        # Create a unique ID for the provision node
        provision_id = f"kp{idx}"
        
        # Create provision node
        provision_cypher = (
            f"CREATE ({provision_id}:KeyProvision {{number: '{number}', "
            f"title: '{title}', "
            f"summary: '{summary}', "
            f"sourceDocument: '{document_name}', "
            f"documentId: '{document_id}' }})"
        )
        cypher_commands.append(provision_cypher)
        
        # Link to contract
        rel_cypher = f"MATCH {contract_ref} CREATE (c)-[:HAS_KEY_PROVISION]->({provision_id})"
        cypher_commands.append(rel_cypher)
    
    return cypher_commands


def generate_financials_cypher(financials: List[Dict[str, Any]],
                             document_name: str,
                             document_id: str) -> List[str]:
    """Generate Cypher commands for financial mentions.
    
    Args:
        financials: List of financial mentions with context
        document_name: Name of the source document
        document_id: Identifier of the source document
        
    Returns:
        List of Cypher commands for financial mentions
    """
    cypher_commands = []
    
    # Find the contract node reference
    contract_ref = "(c:Contract {documentId: '" + document_id + "'})"
    
    for idx, financial in enumerate(financials):
        # Clean text for Cypher query
        amount = financial.get("amount", "").replace("'", "\\'")
        context = financial.get("context", "").replace("'", "\\'")
        
        # Create a unique ID for the financial node
        financial_id = f"f{idx}"
        
        # Create financial node
        financial_cypher = (
            f"CREATE ({financial_id}:Financial {{amount: '{amount}', "
            f"context: '{context}', "
            f"sourceDocument: '{document_name}', "
            f"documentId: '{document_id}' }})"
        )
        cypher_commands.append(financial_cypher)
        
        # Link to contract
        rel_cypher = f"MATCH {contract_ref} CREATE (c)-[:HAS_FINANCIAL]->({financial_id})"
        cypher_commands.append(rel_cypher)
    
    return cypher_commands


def generate_dates_cypher(dates: List[Dict[str, Any]],
                        document_name: str,
                        document_id: str) -> List[str]:
    """Generate Cypher commands for date mentions.
    
    Args:
        dates: List of date mentions with context
        document_name: Name of the source document
        document_id: Identifier of the source document
        
    Returns:
        List of Cypher commands for date mentions
    """
    cypher_commands = []
    
    # Find the contract node reference
    contract_ref = "(c:Contract {documentId: '" + document_id + "'})"
    
    for idx, date in enumerate(dates):
        # Clean text for Cypher query
        date_value = date.get("date", "").replace("'", "\\'")
        context = date.get("context", "").replace("'", "\\'")
        
        # Create a unique ID for the date node
        date_id = f"d{idx}"
        
        # Create date node
        date_cypher = (
            f"CREATE ({date_id}:Date {{value: '{date_value}', "
            f"context: '{context}', "
            f"sourceDocument: '{document_name}', "
            f"documentId: '{document_id}' }})"
        )
        cypher_commands.append(date_cypher)
        
        # Link to contract
        rel_cypher = f"MATCH {contract_ref} CREATE (c)-[:HAS_DATE]->({date_id})"
        cypher_commands.append(rel_cypher)
    
    return cypher_commands


def generate_terms_cypher(terms: Dict[str, List[str]],
                        document_name: str,
                        document_id: str) -> List[str]:
    """Generate Cypher commands for key legal terms.
    
    Args:
        terms: Dictionary of key legal terms with their contexts
        document_name: Name of the source document
        document_id: Identifier of the source document
        
    Returns:
        List of Cypher commands for key legal terms
    """
    cypher_commands = []
    
    # Find the contract node reference
    contract_ref = "(c:Contract {documentId: '" + document_id + "'})"
    
    for term_name, contexts in terms.items():
        # Clean text for Cypher query
        term_name_clean = term_name.replace("'", "\\'")
        
        # Create a sanitized term ID for the node
        term_id = f"t_{term_name.lower().replace(' ', '_')}"
        
        # Create term node with bullet-point formatted contexts
        contexts_clean = []
        for context in contexts:
            contexts_clean.append(context.replace("'", "\\'"))
        
        bullet_points = "• " + "\n• ".join(contexts_clean)
        
        term_cypher = (
            f"CREATE ({term_id}:Term {{name: '{term_name_clean}', "
            f"contexts: '{bullet_points}', "
            f"sourceDocument: '{document_name}', "
            f"documentId: '{document_id}' }})"
        )
        cypher_commands.append(term_cypher)
        
        # Link to contract
        rel_cypher = f"MATCH {contract_ref} CREATE (c)-[:HAS_TERM]->({term_id})"
        cypher_commands.append(rel_cypher)
    
    return cypher_commands


def generate_entities_cypher(entities: Dict[str, List[str]],
                           document_name: str,
                           document_id: str) -> List[str]:
    """Generate Cypher commands for named entities.
    
    Args:
        entities: Dictionary of named entities by entity type
        document_name: Name of the source document
        document_id: Identifier of the source document
        
    Returns:
        List of Cypher commands for named entities
    """
    cypher_commands = []
    
    # Find the contract node reference
    contract_ref = "(c:Contract {documentId: '" + document_id + "'})"
    
    for entity_type, entity_list in entities.items():
        # Clean entity type for Cypher query
        entity_type_clean = entity_type.replace("'", "\\'")
        
        # Create a sanitized entity ID for the node
        entity_id = f"e_{entity_type.lower()}"
        
        # Create entity values as bullet points
        entity_values_clean = []
        for entity in entity_list:
            entity_values_clean.append(entity.replace("'", "\\'"))
        
        bullet_points = "• " + "\n• ".join(entity_values_clean)
        
        entity_cypher = (
            f"CREATE ({entity_id}:Entity {{type: '{entity_type_clean}', "
            f"values: '{bullet_points}', "
            f"sourceDocument: '{document_name}', "
            f"documentId: '{document_id}' }})"
        )
        cypher_commands.append(entity_cypher)
        
        # Link to contract
        rel_cypher = f"MATCH {contract_ref} CREATE (c)-[:HAS_ENTITY]->({entity_id})"
        cypher_commands.append(rel_cypher)
    
    return cypher_commands