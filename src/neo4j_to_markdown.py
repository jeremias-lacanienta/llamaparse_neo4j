#!/usr/bin/env python3
"""
Neo4j to Markdown Converter

Retrieves contract information from Neo4j database and exports it to Markdown format.
This script queries a Neo4j database for contract data based on document ID and
generates a comprehensive contract summary with all key information.

Requirements:
- Neo4j Python driver for database connectivity
- Jinja2 for Markdown templating
"""

import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional
from getpass import getpass

# Import Jinja2 for templating
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Import dotenv for loading environment variables
from dotenv import load_dotenv

# Neo4j imports - assuming libraries are installed
from neo4j import GraphDatabase, basic_auth

# Load environment variables
load_dotenv()


class Neo4jContractReader:
    """Class for retrieving contract data from Neo4j database."""
    
    def __init__(self, uri="bolt://localhost:7687", username="neo4j", password=None):
        """Initialize Neo4j database connection.
        
        Args:
            uri: Neo4j server URI (default: bolt://localhost:7687)
            username: Neo4j username (default: neo4j)
            password: Neo4j password
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = None
        
    def connect(self):
        """Connect to Neo4j database."""
        if not self.password:
            self.password = getpass("Enter Neo4j password: ")
            
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=basic_auth(self.username, self.password)
            )
            print("Connected to Neo4j database")
            return True
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            return False
            
    def close(self):
        """Close the Neo4j database connection."""
        if self.driver:
            self.driver.close()
            print("Neo4j connection closed")
            
    def run_query(self, query, parameters=None):
        """Run a Cypher query.
        
        Args:
            query: Cypher query string
            parameters: Query parameters (optional)
            
        Returns:
            Query results
        """
        if not self.driver:
            raise Exception("Not connected to Neo4j database")
            
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return result.data()

    def get_contract_metadata(self, document_id):
        """Get contract metadata from Neo4j.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            Dictionary with contract metadata
        """
        query = """
        MATCH (c:Contract {documentId: $documentId})
        RETURN c.title as full_title, 
               c.effectiveDate as effective_date, 
               c.documentType as document_type,
               c.sourceDocument as source_document,
               c.importTimestamp as import_timestamp,
               // Use the title as is, we'll clean it in Python
               c.title as title
        """
        
        results = self.run_query(query, {"documentId": document_id})
        
        if not results:
            raise ValueError(f"No contract found with document ID: {document_id}")
        
        # Clean the title
        if "title" in results[0] and results[0]["title"]:
            title = results[0]["title"]
            
            # Extract first line or before ARTICLE text
            if '\n' in title:
                title = title.split('\n')[0].strip()
            if 'ARTICLE' in title:
                title = title.split('ARTICLE')[0].strip()
            if 'Between' in title:
                title = title.split('Between')[0].strip()
                
            # Remove any parenthetical text
            if '(' in title:
                title = title.split('(')[0].strip()
                
            # Remove excessive punctuation
            if title.endswith('.') or title.endswith(':'):
                title = title[:-1].strip()
                
            # Capitalize properly
            if title.isupper():
                title = title.title()
                
            results[0]["title"] = title
            
        return results[0]

    def get_contract_parties(self, document_id):
        """Get contract parties from Neo4j.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            List of party dictionaries with signatories
        """
        # First try the direct relationship pattern
        query = """
        MATCH (p:Party {documentId: $documentId})-[:PARTY_TO]->(c:Contract {documentId: $documentId})
        OPTIONAL MATCH (s:Person)-[:REPRESENTS]->(p)
        WITH p.name as party_name, p.type as party_type, 
             collect({name: s.name, title: s.title}) as signatories
        RETURN party_name, party_type, signatories
        """
        
        results = self.run_query(query, {"documentId": document_id})
        
        # If no results, get the Party nodes directly using more generic criteria
        if not results:
            query = """
            MATCH (p:Party {documentId: $documentId})
            WHERE p.name IS NOT NULL 
            AND size(p.name) > 3
            AND NOT p.name IN ['', 'A', 'B', 'C', 'The']
            RETURN DISTINCT p.name as party_name, p.type as party_type, [] as signatories
            ORDER BY 
            CASE 
                WHEN p.name CONTAINS "Inc." OR p.name CONTAINS "Corporation" OR p.name CONTAINS "LLC" THEN 0
                WHEN p.name CONTAINS "B.V." OR p.name CONTAINS "GmbH" OR p.name CONTAINS "Ltd" THEN 1
                ELSE 2
            END DESC
            LIMIT 5
            """
            results = self.run_query(query, {"documentId": document_id})
        
        # Clean up party names
        parties = []
        for result in results:
            name = result["party_name"]
            # Remove embedded line breaks
            if name and "\n" in name:
                name = name.split("\n")[0]
            # Remove embedded parenthetical
            if name and "(" in name:
                name = name.split("(")[0].strip()
            
            if name:
                parties.append({
                    "name": name,
                    "type": result["party_type"],
                    "signatories": [sig for sig in result["signatories"] if sig["name"] is not None]
                })
            
        return parties

    def get_contract_articles(self, document_id):
        """Get contract articles and sections from Neo4j.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            List of article dictionaries with sections
        """
        query = """
        MATCH (c:Contract {documentId: $documentId})-[:CONTAINS]->(a:Article)
        OPTIONAL MATCH (a)-[:HAS_SECTION]->(s:Section)
        WITH a.number as article_number, a.title as article_title,
             collect({number: s.number, title: s.title, content: s.content}) as sections
        ORDER BY article_number
        RETURN article_number, article_title, sections
        """
        
        results = self.run_query(query, {"documentId": document_id})
        
        articles = []
        for result in results:
            articles.append({
                "number": result["article_number"],
                "title": result["article_title"],
                "sections": [section for section in result["sections"] if section["number"] is not None]
            })
            
        return articles

    def get_key_provisions(self, document_id):
        """Get key provisions from Neo4j.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            List of key provision dictionaries
        """
        # Try standard relationship for key provisions
        query = """
        MATCH (c:Contract {documentId: $documentId})-[:HAS_KEY_PROVISION]->(kp:KeyProvision)
        RETURN kp.number as number, kp.title as title, kp.summary as summary
        """
        
        results = self.run_query(query, {"documentId": document_id})
        
        # If no results, try to extract from article section relationships with more generic approach
        if not results:
            query = """
            MATCH (c:Contract {documentId: $documentId})-[:CONTAINS]->(a)-[:HAS_SECTION]->(s)
            WHERE LOWER(a.title) CONTAINS 'purpose' OR LOWER(a.title) CONTAINS 'scope' OR 
                  LOWER(a.title) CONTAINS 'license' OR LOWER(a.title) CONTAINS 'term' OR
                  LOWER(a.title) CONTAINS 'payment' OR LOWER(a.title) CONTAINS 'termination' OR
                  LOWER(a.title) CONTAINS 'background' OR LOWER(a.title) CONTAINS 'recital' OR
                  LOWER(a.title) CONTAINS 'definitions' OR LOWER(a.title) CONTAINS 'objective'
            RETURN a.number as number, a.title as title, 
                   substring(s.content, 0, 200) + '...' as summary
            LIMIT 5
            """
            results = self.run_query(query, {"documentId": document_id})
        
        # If still no results, extract dynamic information from the contract metadata and entities
        if not results:
            query = """
            MATCH (c:Contract {documentId: $documentId})
            WITH c
            OPTIONAL MATCH (c)-[:HAS_FINANCIAL]->(f:Financial) 
            WITH c, collect(DISTINCT f.context)[0] as financial_context
            OPTIONAL MATCH (c)-[:HAS_DATE]->(d:Date) 
            WITH c, financial_context, collect(DISTINCT d.context)[0] as date_context
            OPTIONAL MATCH (p:Party {documentId: $documentId})
            WHERE p.name IS NOT NULL AND size(p.name) > 3 
            AND NOT p.name IN ['', 'A', 'B', 'C', 'The']
            WITH c, financial_context, date_context, collect(DISTINCT p.name) as party_names
            
            // Use the title as is - we'll clean it in Python
            WITH c, financial_context, date_context, party_names, c.title as clean_title
            
            // Extract key terms to describe the agreement purpose
            OPTIONAL MATCH (c)-[:CONTAINS]->(a:Article)
            WHERE LOWER(a.title) CONTAINS 'purpose' OR LOWER(a.title) CONTAINS 'scope'
            WITH c, financial_context, date_context, party_names, clean_title, 
                 collect(a.title)[0] as purpose_article
                 
            RETURN 'Main' as number, 
                   // Just use the clean title as is
                   clean_title as title,
                   
                   // Create a clean summary without duplicating metadata already shown elsewhere
                   'This ' + 
                   CASE WHEN c.documentType IS NOT NULL 
                        THEN LOWER(c.documentType) 
                        ELSE 'agreement' 
                   END + 
                   
                   CASE WHEN SIZE(party_names) >= 2 
                        THEN ' between ' + party_names[0] + ' and ' + party_names[1]
                        WHEN SIZE(party_names) = 1
                        THEN ' involving ' + party_names[0]
                        ELSE ' between the involved parties'
                   END + 
                   
                   ' establishes terms for ' +
                   
                   // Use a more generic approach based on document type and property patterns
                   CASE 
                        WHEN c.documentType IS NOT NULL
                        THEN 'a ' + LOWER(c.documentType) + ' arrangement'
                        WHEN purpose_article IS NOT NULL 
                        THEN 'activities related to ' + LOWER(purpose_article)
                        ELSE 'business operations between the parties'
                   END + 
                   
                   '. ' +
                   
                   CASE WHEN financial_context IS NOT NULL 
                        THEN 'Financial terms include ' + financial_context + '. '
                        ELSE ''
                   END as summary
            """
            results = self.run_query(query, {"documentId": document_id})
        
        provisions = []
        for result in results:
            # Clean the title if present
            title = result["title"] if result["title"] else "Key Provision"
            if title:
                # Extract first line or before ARTICLE text
                if '\n' in title:
                    title = title.split('\n')[0].strip()
                if 'ARTICLE' in title:
                    title = title.split('ARTICLE')[0].strip()
                    
                # If the title is just a number, add "Article"
                if title.strip().isdigit():
                    title = f"Article {title.strip()}"
                    
                # Remove excessive punctuation
                if title.endswith('.') or title.endswith(':'):
                    title = title[:-1].strip()
                    
                # Capitalize properly
                if title.isupper():
                    title = title.title()
            
            provisions.append({
                "number": result["number"],
                "title": title,
                "summary": result["summary"] if result["summary"] else "No summary available."
            })
            
        return provisions

    def get_financials(self, document_id):
        """Get financial mentions from Neo4j.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            List of financial mention dictionaries
        """
        query = """
        MATCH (c:Contract {documentId: $documentId})-[:HAS_FINANCIAL]->(f:Financial)
        RETURN f.amount as amount, f.context as context
        """
        
        results = self.run_query(query, {"documentId": document_id})
        
        financials = []
        for result in results:
            financials.append({
                "amount": result["amount"],
                "context": result["context"]
            })
            
        return financials

    def get_key_dates(self, document_id):
        """Get key dates from Neo4j.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            List of date mention dictionaries
        """
        query = """
        MATCH (c:Contract {documentId: $documentId})-[:HAS_DATE]->(d:Date)
        RETURN d.value as date, d.context as context
        """
        
        results = self.run_query(query, {"documentId": document_id})
        
        dates = []
        for result in results:
            dates.append({
                "date": result["date"],
                "context": result["context"]
            })
            
        return dates

    def get_key_terms(self, document_id):
        """Get key terms from Neo4j.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            Dictionary of term names and contexts
        """
        query = """
        MATCH (c:Contract {documentId: $documentId})-[:HAS_TERM]->(t:Term)
        RETURN t.name as name, t.contexts as contexts
        """
        
        results = self.run_query(query, {"documentId": document_id})
        
        terms = {}
        for result in results:
            # Split bullet points back into a list
            contexts = result["contexts"].split("\n• ")
            # Clean up the first item which has the bullet point
            if contexts and contexts[0].startswith("• "):
                contexts[0] = contexts[0][2:]
                
            terms[result["name"]] = contexts
            
        return terms

    def get_named_entities(self, document_id):
        """Get named entities from Neo4j.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            Dictionary of entity types and values
        """
        query = """
        MATCH (c:Contract {documentId: $documentId})-[:HAS_ENTITY]->(e:Entity)
        RETURN e.type as type, e.values as values
        """
        
        results = self.run_query(query, {"documentId": document_id})
        
        entities = {}
        for result in results:
            # Split bullet points back into a list
            values = result["values"].split("\n• ")
            # Clean up the first item which has the bullet point
            if values and values[0].startswith("• "):
                values[0] = values[0][2:]
                
            entities[result["type"]] = values
            
        return entities

    def get_contract_info(self, document_id):
        """Get all contract information from Neo4j.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            Dictionary with all contract information
        """
        try:
            contract_info = {
                "metadata": self.get_contract_metadata(document_id),
                "parties": self.get_contract_parties(document_id),
                "articles": self.get_contract_articles(document_id),
                "key_provisions": self.get_key_provisions(document_id),
                "financials": self.get_financials(document_id),
                "key_dates": self.get_key_dates(document_id),
                "key_terms": self.get_key_terms(document_id),
                "named_entities": self.get_named_entities(document_id)
            }
            
            return contract_info
        except Exception as e:
            print(f"Error retrieving contract information: {e}")
            raise


def generate_markdown(contract_info: Dict[str, Any], output_file: str):
    """Generate a Markdown file with the contract information using Jinja2 templating.
    
    Args:
        contract_info: Dictionary containing the contract information
        output_file: Path to the output Markdown file
    """
    # Determine the templates path relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(os.path.dirname(script_dir), "templates")
    
    # Load Jinja2 template
    env = Environment(
        loader=FileSystemLoader(searchpath=templates_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template("contract_summary.md.j2")
    
    # Render template with contract information
    rendered_md = template.render(
        key_info=contract_info,
        generated_on=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        source="Neo4j Database"
    )
    
    # Write to output file
    with open(output_file, 'w') as f:
        f.write(rendered_md)
    
    print(f"Successfully generated Markdown summary: {output_file}")


def main():
    """Main function to process command line arguments."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Retrieve contract info from Neo4j and export to Markdown')
    parser.add_argument('--document-id', '-d', type=str, default="sample_contract_enhanced",
                        help='Document ID to retrieve from Neo4j')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='Path to the output Markdown file')
    parser.add_argument('--uri', '-u', type=str, default="bolt://localhost:7687",
                        help='Neo4j server URI')
    parser.add_argument('--user', type=str, default="neo4j",
                        help='Neo4j username')
    parser.add_argument('--password', '-p', type=str, default=None,
                        help='Neo4j password (if not provided, will prompt)')
    
    # Parse arguments
    args = parser.parse_args()
    document_id = args.document_id
    neo4j_uri = args.uri
    neo4j_user = args.user
    neo4j_password = args.password
    
    # Set default output file path if not provided
    output_file = args.output if args.output else f"./data/{document_id}_summary.md"
    
    # Create Neo4j reader and connect
    reader = Neo4jContractReader(
        uri=neo4j_uri,
        username=neo4j_user,
        password=neo4j_password
    )
    
    if not reader.connect():
        sys.exit(1)
    
    try:
        # Get contract information from Neo4j
        print(f"Retrieving contract information for document ID: {document_id}")
        contract_info = reader.get_contract_info(document_id)
        
        # Generate markdown summary
        generate_markdown(contract_info, output_file)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        reader.close()


if __name__ == "__main__":
    main()
