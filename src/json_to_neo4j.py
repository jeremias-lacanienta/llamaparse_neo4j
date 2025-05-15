#!/usr/bin/env python3
"""
JSON to Neo4j Converter

This script converts LlamaParse JSON output to Neo4j Cypher commands for importing
contract data into a graph database. Uses SpaCy and ContractBERT for enhanced legal text processing.
Extracts comprehensive contract information including key provisions, financial terms,
key dates, legal terminology, and named entities.
"""

import json
import os
import sys
import re
import argparse
import spacy
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import ContractBERT/transformer libraries
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline, AutoModelForSequenceClassification

# Import extraction functions from extract package
from extract import extract_contract_metadata, extract_articles, extract_parties
from extract.txt_parser import (
    read_txt_file, extract_articles_from_text, 
    extract_contract_metadata_from_text
)

# Import Cypher generation functionality
from cypher_generator import process_json_file

# Import constants
from contract_constants import (
    DATE_CONTEXTS, FINANCIAL_PATTERNS, DATE_PATTERNS, KEY_TERM_PATTERNS
)

# Load SpaCy model - using the large model for better accuracy
nlp = spacy.load("en_core_web_lg")

# Global variables for ContractBERT models
contractbert_ner = None
contractbert_classifier = None
contractbert_tokenizer = None

def initialize_contractbert():
    """Initialize the ContractBERT models for contract analysis."""
    global contractbert_ner, contractbert_classifier, nlp
    
    # Load ContractBERT NER model
    try:
        # Initialize ContractBERT for named entity recognition using legal-bert
        # Note: Using nlpaueb/legal-bert-base-uncased which is available on HuggingFace
        contractbert_ner = pipeline(
            "token-classification", 
            model="nlpaueb/legal-bert-base-uncased", 
            aggregation_strategy="simple"
        )
        
        # Initialize ContractBERT for text classification
        contractbert_classifier = pipeline(
            "text-classification",
            model="nlpaueb/legal-bert-base-uncased"
        )
        
        # Initialize SpaCy for additional NLP tasks
        nlp = spacy.load("en_core_web_lg")
        
        return True
    except Exception as e:
        print(f"Error initializing ContractBERT models: {e}", file=sys.stderr)
        # Initialize fallback functions instead of None to avoid NoneType errors
        contractbert_ner = lambda x: []
        contractbert_classifier = lambda x: [{"label": "UNKNOWN", "score": 0.0}]
        return False

def classify_contract_clauses(text):
    """Use ContractBERT to classify contract clauses by type."""
    # Split text into chunks of appropriate size for ContractBERT
    chunks = [text[i:i+450] for i in range(0, len(text), 450)]
    
    clause_types = {
        "DEFINITION": [],
        "OBLIGATION": [],
        "CONDITION": [],
        "TERM": [],
        "PAYMENT": []
    }
    
    for chunk in chunks:
        # Process chunk with ContractBERT
        classification = contractbert_classifier(chunk)
        
        # Map classification label to clause type
        label = classification[0]["label"]
        score = classification[0]["score"]
        
        # Only consider classifications with reasonable confidence
        if score > 0.6:
            if "DEFINITION" in label:
                clause_types["DEFINITION"].append((chunk, score))
            elif "OBLIGATION" in label:
                clause_types["OBLIGATION"].append((chunk, score))
            elif "CONDITION" in label:
                clause_types["CONDITION"].append((chunk, score))
            elif "TERM" in label:
                clause_types["TERM"].append((chunk, score))
            elif "PAYMENT" in label:
                clause_types["PAYMENT"].append((chunk, score))
    
    return clause_types

def identify_contract_elements(doc):
    """Use spaCy and ContractBERT to identify contract elements in text."""
    elements = {
        "definitions": [],
        "obligations": [],
        "conditions": [],
        "terms": [],
        "payments": []
    }
    
    # Process each sentence with ContractBERT for classification
    for sent in doc.sents:
        if len(sent.text.strip()) < 10:  # Skip very short sentences
            continue
            
        # Classify sentence
        classification = contractbert_classifier(sent.text[:min(len(sent.text), 450)])
        label = classification[0]["label"]
        score = classification[0]["score"]
        
        if score > 0.6:
            if "DEFINITION" in label:
                elements["definitions"].append(sent.text)
            elif "OBLIGATION" in label or "REQUIREMENT" in label:
                elements["obligations"].append(sent.text)
            elif "CONDITION" in label:
                elements["conditions"].append(sent.text)
            elif "TERM" in label:
                elements["terms"].append(sent.text)
            elif "PAYMENT" in label or "FINANCIAL" in label:
                elements["payments"].append(sent.text)
    
    return elements

def get_full_text(data: List[Dict[str, Any]]) -> str:
    """Extract full text from all pages of the contract."""
    full_text = ""
    if data and len(data) > 0 and "pages" in data[0]:
        for page in data[0]["pages"]:
            full_text += page.get("text", "") + " "
    return full_text


def extract_named_entities(data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Extract named entities from the contract using SpaCy and ContractBERT."""
    entities = {
        "PERSON": [],
        "ORG": [],
        "DATE": [],
        "MONEY": [],
        "LAW": [],
        "GPE": []  # Geopolitical entities (locations)
    }
    
    full_text = get_full_text(data)
    
    # Process with ContractBERT for legal-specific entities
    # Process text in chunks to avoid context length issues
    chunk_size = 450
    text_chunks = [full_text[i:i+chunk_size] for i in range(0, min(len(full_text), 10000), chunk_size)]
    
    for chunk in text_chunks:
        results = contractbert_ner(chunk)
        for entity in results:
            entity_type = entity.get("entity_group", "")
            word = entity.get("word", "")
            if entity_type in entities and word not in entities[entity_type]:
                entities[entity_type].append(word)
    
    # Process with SpaCy for additional entities
    # Process text in chunks to avoid memory issues
    chunk_size = 5000
    for i in range(0, min(len(full_text), 25000), chunk_size):
        chunk = full_text[i:i+chunk_size]
        doc = nlp(chunk)
        
        for ent in doc.ents:
            if ent.label_ in entities and ent.text not in entities[ent.label_]:
                # Clean up and deduplicate entities
                clean_text = re.sub(r'\s+', ' ', ent.text).strip()
                if clean_text and len(clean_text) > 1:  # Avoid single characters
                    entities[ent.label_].append(clean_text)
    
    # Filter out empty categories
    return {k: v for k, v in entities.items() if v}


def extract_key_provisions(data: List[Dict[str, Any]], articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract key provisions from the contract using ContractBERT classification."""
    key_provisions = []
    
    # Use ContractBERT to classify important provisions
    important_keywords = [
        'scope', 'purpose', 'term', 'payment', 'confidential', 'intellectual property',
        'termination', 'governing law', 'indemnification', 'warranty', 'liability',
        'obligations', 'representations', 'warranties', 'compliance', 'assignment'
    ]
    
    for article in articles:
        article_title = article.get('title', '').lower()
        article_number = article.get('number', '')
        
        # Check if the article contains important keywords
        is_important = any(keyword in article_title for keyword in important_keywords)
        
        # For articles that don't match keywords, use ContractBERT to classify importance
        if not is_important and article.get('content'):
            # Process article content with ContractBERT
            article_text = article.get('content', '')
            # Process in chunks if too long
            if len(article_text) > 450:
                chunks = [article_text[i:i+450] for i in range(0, min(len(article_text), 2000), 450)]
                for chunk in chunks:
                    classification = contractbert_classifier(chunk)
                    label = classification[0]["label"]
                    score = classification[0]["score"]
                    
                    # Check if the classification suggests an important provision
                    if score > 0.7 and any(keyword in label.lower() for keyword in important_keywords):
                        is_important = True
                        break
            else:
                # Process small articles directly
                classification = contractbert_classifier(article_text)
                label = classification[0]["label"]
                score = classification[0]["score"]
                if score > 0.7 and any(keyword in label.lower() for keyword in important_keywords):
                    is_important = True
        
        if is_important:
            # Get a summary of the article by joining the first part of each section
            summary = ""
            for section in article.get('sections', []):
                section_content = section.get('content', '')
                if section_content:
                    # Add first sentence or first 100 characters
                    first_sentence = section_content.split('.')[0] + '.'
                    summary += f"{section.get('number', '')}: {first_sentence} "
                    if len(summary) > 300:
                        summary = summary[:300] + "..."
                        break
            
            key_provisions.append({
                "number": article_number,
                "title": article.get('title', ''),
                "summary": summary
            })
    
    return key_provisions


def extract_financials_with_nlp(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract financial terms using SpaCy and ContractBERT."""
    financials = []
    full_text = get_full_text(data)
    
    # Use ContractBERT for money entity extraction
    chunk_size = 450
    text_chunks = [full_text[i:i+chunk_size] for i in range(0, min(len(full_text), 10000), chunk_size)]
    
    for chunk in text_chunks:
        results = contractbert_ner(chunk)
        for entity in results:
            if entity["entity_group"] == "MONEY":
                # Get surrounding context (use the start/end from the entity)
                start_idx = max(0, entity["start"] - 50)
                end_idx = min(len(chunk), entity["end"] + 50)
                context = chunk[start_idx:end_idx]
                context = re.sub(r'\s+', ' ', context).strip()
                
                financials.append({
                    "amount": entity["word"],
                    "context": context
                })
    
    # Use SpaCy for additional money entity extraction
    # Process text in chunks
    chunk_size = 5000
    money_entities = []
    
    for i in range(0, min(len(full_text), 25000), chunk_size):
        chunk = full_text[i:i+chunk_size]
        doc = nlp(chunk)
        
        # Extract money entities and their context
        for ent in doc.ents:
            if ent.label_ == "MONEY":
                # Get surrounding context (use the sentence for better context)
                context = ent.sent.text if hasattr(ent, 'sent') else chunk[max(0, ent.start_char-50):min(len(chunk), ent.end_char+50)]
                
                money_entities.append({
                    "amount": ent.text,
                    "context": re.sub(r'\s+', ' ', context).strip()
                })
    
    # Add SpaCy entities to results
    if money_entities:
        seen_amounts = set()
        for entity in money_entities:
            if entity["amount"] not in seen_amounts:
                financials.append(entity)
                seen_amounts.add(entity["amount"])
    
    return financials[:15]  # Limit to top 15 financial mentions


def extract_dates_with_nlp(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract key dates using SpaCy and ContractBERT."""
    key_dates = []
    full_text = get_full_text(data)
    
    # Use ContractBERT for date entity extraction
    chunk_size = 450
    text_chunks = [full_text[i:i+chunk_size] for i in range(0, min(len(full_text), 10000), chunk_size)]
    
    for chunk in text_chunks:
        results = contractbert_ner(chunk)
        for entity in results:
            if entity["entity_group"] == "DATE":
                # Get surrounding context (use the start/end from the entity)
                start_idx = max(0, entity["start"] - 50)
                end_idx = min(len(chunk), entity["end"] + 50)
                context = chunk[start_idx:end_idx]
                context = re.sub(r'\s+', ' ', context).strip()
                
                key_dates.append({
                    "date": entity["word"],
                    "context": context
                })
    
    # Use SpaCy for additional date entity extraction
    chunk_size = 5000
    date_entities = []
    
    for i in range(0, min(len(full_text), 25000), chunk_size):
        chunk = full_text[i:i+chunk_size]
        doc = nlp(chunk)
        
        # Extract date entities and their context
        for ent in doc.ents:
            if ent.label_ == "DATE":
                # Get surrounding context (use the sentence for better context)
                context = ent.sent.text if hasattr(ent, 'sent') else chunk[max(0, ent.start_char-50):min(len(chunk), ent.end_char+50)]
                
                date_entities.append({
                    "date": ent.text,
                    "context": re.sub(r'\s+', ' ', context).strip()
                })
    
    # Add SpaCy entities to results
    if date_entities:
        seen_dates = set()
        for entity in date_entities:
            if entity["date"] not in seen_dates:
                key_dates.append(entity)
                seen_dates.add(entity["date"])
    
    return key_dates[:15]  # Limit to top 15 date mentions


def extract_key_terms(data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Extract key legal terms and their contexts using ContractBERT."""
    key_terms = {}
    full_text = get_full_text(data)
    
    # Use ContractBERT to classify text chunks by legal term type
    term_classifications = {
        'effective date': [],
        'termination': [],
        'confidentiality': [],
        'intellectual property': [],
        'payment terms': [],
        'dispute resolution': [],
        'governing law': [],
        'force majeure': [],
        'indemnification': [],
        'limitation of liability': [],
        'warranty': []
    }
    
    # Process text in chunks with ContractBERT
    chunk_size = 450
    chunks = [full_text[i:i+chunk_size] for i in range(0, min(len(full_text), 25000), chunk_size)]
    
    for chunk in chunks:
        # Skip very short chunks
        if len(chunk.strip()) < 20:
            continue
        
        try:    
            # Classify chunk
            classification = contractbert_classifier(chunk)
            label = classification[0]["label"]
            score = classification[0]["score"]
            
            # Match classification to term types
            if score > 0.6:
                for term in term_classifications.keys():
                    if term in label.lower() or any(word in label.lower() for word in term.split()):
                        term_classifications[term].append(chunk)
                        break
        except Exception as e:
            print(f"Warning: Error classifying chunk: {e}")
            continue
    
    # Use ContractBERT results only - no regex fallback for consistent processing
    for term, contexts in term_classifications.items():
        if contexts:
            key_terms[term] = contexts[:3]  # Limit to 3 contexts per term
    
    return key_terms

def process_with_fallback(json_file: str, txt_file: str) -> Dict[str, Any]:
    """
    Process contract data with fallback to TXT file if JSON structure has issues.
    
    Args:
        json_file: Path to the LlamaParse JSON file
        txt_file: Path to the corresponding TXT file for fallback
        
    Returns:
        Processed contract data with extracted information
    """
    print(f"Processing contract data from {json_file}")
    
    # Initialize container for processed data
    processed_data = {
        "metadata": {},
        "articles": [],
        "parties": [],
        "entities": [],
        "definitions": [],
        "source": "json"  # Track the source of extraction
    }
    
    # Try to load and process JSON first
    json_success = True
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Check if JSON has the expected structure
        if "pages" not in json_data or not json_data.get("pages"):
            print("Warning: JSON file missing 'pages' structure, will use TXT fallback")
            json_success = False
        elif not any(page.get("text") for page in json_data.get("pages", [])):
            print("Warning: JSON file has empty or missing text in pages, will use TXT fallback")
            json_success = False
        else:
            # Attempt to extract information from JSON
            try:
                # Extract metadata
                metadata = extract_contract_metadata([json_data])
                processed_data["metadata"] = metadata
                
                # Extract articles and sections
                articles = extract_articles([json_data], nlp, contractbert_ner)
                processed_data["articles"] = articles
                
                # Extract parties
                parties = extract_parties([json_data])
                processed_data["parties"] = parties
                
                # Basic validation of extraction quality
                if not processed_data["articles"]:
                    print("Warning: Failed to extract articles from JSON, will try TXT fallback")
                    json_success = False
                elif not any(article.get("content") for article in processed_data["articles"]):
                    print("Warning: Extracted articles have no content, will try TXT fallback")
                    json_success = False
            except Exception as e:
                print(f"Error during JSON extraction: {e}")
                json_success = False
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        json_success = False
    
    # If JSON processing failed and TXT file is provided, use TXT fallback
    if not json_success and txt_file and os.path.exists(txt_file):
        print(f"Using TXT fallback extraction from {txt_file}")
        try:
            # Read TXT file
            txt_content = read_txt_file(txt_file)
            
            # Extract metadata from TXT
            metadata = extract_contract_metadata_from_text(txt_content)
            processed_data["metadata"] = metadata
            
            # Extract articles and sections from TXT
            articles = extract_articles_from_text(txt_content)
            processed_data["articles"] = articles
            
            processed_data["source"] = "txt"  # Update source to reflect TXT extraction
            
            print("Successfully extracted contract data using TXT fallback")
        except Exception as e:
            print(f"Error during TXT fallback extraction: {e}")
            if not processed_data["articles"]:
                # If both JSON and TXT extraction failed, raise an exception
                raise RuntimeError(f"Failed to extract contract data from both JSON and TXT: {e}")
    
    # Implement a hybrid approach if JSON was successful but some parts are missing
    if json_success and txt_file and os.path.exists(txt_file):
        # Check if we need to supplement JSON data with TXT data
        if not processed_data["articles"] or not processed_data["metadata"] or not processed_data["metadata"].get("title"):
            print("Using hybrid approach to supplement JSON with TXT data")
            try:
                txt_content = read_txt_file(txt_file)
                
                # If articles are missing, extract from TXT
                if not processed_data["articles"]:
                    articles = extract_articles_from_text(txt_content)
                    processed_data["articles"] = articles
                
                # If metadata is incomplete, supplement from TXT
                if not processed_data["metadata"].get("document_type") or not processed_data["metadata"].get("effective_date") or not processed_data["metadata"].get("title"):
                    txt_metadata = extract_contract_metadata_from_text(txt_content)
                    
                    # Update missing fields
                    if not processed_data["metadata"].get("document_type"):
                        processed_data["metadata"]["document_type"] = txt_metadata.get("document_type")
                    
                    if not processed_data["metadata"].get("effective_date"):
                        processed_data["metadata"]["effective_date"] = txt_metadata.get("effective_date")
                    
                    if not processed_data["metadata"].get("execution_date"):
                        processed_data["metadata"]["execution_date"] = txt_metadata.get("execution_date")
                    
                    # Add title if missing or is empty string
                    if not processed_data["metadata"].get("title"):
                        processed_data["metadata"]["title"] = txt_metadata.get("title", "Untitled Contract")
                
                processed_data["source"] = "hybrid"  # Update source to reflect hybrid extraction
            except Exception as e:
                print(f"Warning: Error during hybrid extraction: {e}")
    
    return processed_data

def main():
    """Main entry point for the script."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert contract JSON to Neo4j Cypher commands')
    parser.add_argument('--input', '-i', type=str, default="./data/sample_contract_enhanced.json",
                        help='Path to the input JSON file')
    parser.add_argument('--txt', '-t', type=str, default="./data/sample_contract.txt",
                        help='Path to the fallback TXT file')
    parser.add_argument('--output', '-o', type=str, default="./data/sample_contract_enhanced.cypher",
                        help='Path to the output Cypher file')
    
    # Parse arguments
    args = parser.parse_args()
    input_file = args.input
    txt_file = args.txt
    output_file = args.output
    
    # Initialize ContractBERT
    print("Initializing ContractBERT for legal text analysis...")
    if not initialize_contractbert():
        print("Warning: Using fallback NLP processing due to ContractBERT initialization failure.")
    
    try:
        # Process with fallback strategy
        processed_data = process_with_fallback(input_file, txt_file)
        
        # Extract articles, metadata and parties from processed data
        metadata = processed_data.get("metadata", {})
        articles = processed_data.get("articles", [])
        parties = processed_data.get("parties", [])
        
        # Log the source of extraction
        print(f"Data extraction source: {processed_data.get('source', 'unknown')}")
        
        # Extract additional information
        key_provisions = extract_key_provisions([{"articles": articles}], articles)
        financials = extract_financials_with_nlp([{"articles": articles}])
        dates = extract_dates_with_nlp([{"articles": articles}])
        terms = extract_key_terms([{"articles": articles}])
        entities = extract_named_entities([{"articles": articles}])
        
        # Call the process_json_file function with all extracted information
        process_json_file(
            input_file, 
            output_file,
            metadata,
            articles,
            parties,
            key_provisions,
            financials,
            dates,
            terms,
            entities
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
if __name__ == "__main__":
    main()