#!/usr/bin/env python3
"""
Key Contract Information Extractor

Extracts key information from contract JSON data and exports to Markdown.
This script builds on the existing extraction modules to create a comprehensive
contract summary with financial terms, key dates, and important legal provisions.

Requirements:
- SpaCy with en_core_web_lg model
- Transformers library with ContractBERT models
- Jinja2 for Markdown templating
"""

import os
import json
import re
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import existing extraction modules
from extract.metadata import extract_contract_metadata
from extract.parties import extract_parties
from extract.articles import extract_articles

# Import constants
from contract_constants import (
    DATE_CONTEXTS, FINANCIAL_PATTERNS, DATE_PATTERNS, KEY_TERM_PATTERNS
)

import spacy
from transformers import pipeline
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Initialize NLP models
nlp = spacy.load("en_core_web_lg")
contractbert_ner = None
contractbert_classifier = None

def load_nlp_models():
    """Load SpaCy and ContractBERT models."""
    global nlp, contractbert_ner, contractbert_classifier
    
    print("Loading SpaCy en_core_web_lg model...")
    
    # Load ContractBERT models
    print("Loading ContractBERT NER model...")
    contractbert_ner = pipeline("token-classification", model="nlpaueb/legal-bert-base-uncased", aggregation_strategy="simple")
    print("ContractBERT NER model loaded successfully.")
    
    print("Loading ContractBERT classifier model...")
    contractbert_classifier = pipeline("text-classification", model="nlpaueb/legal-bert-base-uncased")
    print("ContractBERT classifier model loaded successfully.")

def extract_key_information(json_file: str) -> Dict[str, Any]:
    """Extract key information from the contract JSON file.
    
    Args:
        json_file: Path to the JSON file containing contract data
        
    Returns:
        Dictionary with extracted key information
    """
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Load NLP models if not already loaded
    if contractbert_ner is None:
        load_nlp_models()
    
    # Extract information using existing modules with NLP enhancement
    metadata = extract_contract_metadata(data, nlp=nlp, 
                                    contractbert_ner=contractbert_ner, 
                                    contractbert_classifier=contractbert_classifier)
    parties = extract_parties(data, nlp, contractbert_ner)
    articles = extract_articles(data, nlp, contractbert_ner)
    
    # Extract additional key information
    result = {
        "metadata": metadata,
        "parties": parties,
        "key_provisions": extract_key_provisions(data, articles),
        "financials": extract_financials_with_nlp(data),
        "key_dates": extract_dates_with_nlp(data),
        "key_terms": extract_key_terms(data),
        "named_entities": extract_named_entities(data)
    }
    
    return result


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
    full_text = get_full_text(data)
    
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
    
    # If no results from ContractBERT, use key term patterns for fallback
    if all(len(contexts) == 0 for contexts in term_classifications.values()):
        # Find key term patterns
        for term_name, pattern in KEY_TERM_PATTERNS.items():
            matches = re.finditer(pattern, full_text, re.IGNORECASE)
            contexts = []
            
            for match in matches:
                # Get surrounding context (80 chars before and after)
                start_idx = max(0, match.start() - 80)
                end_idx = min(len(full_text), match.end() + 80)
                context = full_text[start_idx:end_idx]
                
                # Clean up context
                context = re.sub(r'\s+', ' ', context).strip()
                contexts.append(context)
            
            if contexts:
                key_terms[term_name] = contexts[:3]  # Limit to 3 contexts per term
    else:
        # Use ContractBERT results
        for term, contexts in term_classifications.items():
            if contexts:
                key_terms[term] = contexts[:3]  # Limit to 3 contexts per term
    
    return key_terms


def generate_markdown(key_info: Dict[str, Any], output_file: str):
    """Generate a Markdown file with the extracted key information using Jinja2 templating.
    
    Args:
        key_info: Dictionary containing the extracted key information
        output_file: Path to the output Markdown file
    """
    # Load Jinja2 template with correct path for when running from project root
    env = Environment(
        loader=FileSystemLoader(searchpath="templates"),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template("contract_summary.md.j2")
    
    # Render template with key information
    rendered_md = template.render(key_info=key_info, generated_on=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Write to output file
    with open(output_file, 'w') as f:
        f.write(rendered_md)


def main():
    """Main function to process command line arguments."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract key information from contract JSON data')
    parser.add_argument('--input', '-i', type=str, default="./data/sample_contract_enhanced.json",
                        help='Path to the input JSON file containing contract data')
    parser.add_argument('--output', '-o', type=str, default="./data/sample_contract_key_info.md",
                        help='Path to the output Markdown file for the extracted information')
    
    # Parse arguments
    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    
    # Extract information and generate Markdown
    try:
        print(f"Extracting key information from: {input_file}")
        key_info = extract_key_information(input_file)
        generate_markdown(key_info, output_file)
        print(f"Successfully generated Markdown summary: {output_file}")
    except Exception as e:
        print(f"Error processing contract: {e}")
        raise

if __name__ == "__main__":
    main()