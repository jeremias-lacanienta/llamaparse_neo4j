#!/usr/bin/env python3
"""
Metadata Extraction Module

This module handles extraction of contract metadata like titles, dates,
document types, and parties from the parsed contract JSON.
"""

import re
from typing import Dict, List, Any

from contract_constants import (
    TITLE_PATTERNS, DOC_TYPES, DATE_CONTEXTS, PARTY_INDICATORS
)


def extract_contract_metadata(data: List[Dict[str, Any]], nlp=None, 
                             contractbert_ner=None, contractbert_classifier=None) -> Dict[str, Any]:
    """Extract key metadata about the contract using ContractBERT and SpaCy NLP for better accuracy.
    
    Args:
        data: The parsed contract JSON data
        nlp: The SpaCy NLP model
        contractbert_ner: The ContractBERT NER model (optional)
        contractbert_classifier: The ContractBERT classifier model (optional)
        
    Returns:
        Dictionary containing contract metadata
    """
    metadata = {"title": "", "effective_date": "", "parties": [], "document_type": "Contract"}
    
    # Check for document metadata in the first page
    if data and len(data) > 0 and "pages" in data[0]:
        first_page_text = data[0]["pages"][0]["text"]
        
        # Process with ContractBERT if available
        if contractbert_ner is not None:
            # Process the text with ContractBERT in chunks
            chunk_size = 450  # Leave buffer for special tokens
            text_chunks = [first_page_text[i:i+chunk_size] for i in range(0, min(len(first_page_text), 10000), chunk_size)]
            
            # Extract entities using ContractBERT
            entities = {"DATE": [], "ORG": [], "PERSON": [], "MONEY": [], "TIME": []}
            
            print("Analyzing contract with ContractBERT...")
            for chunk in text_chunks:
                try:
                    # Apply NER pipeline to each chunk
                    results = contractbert_ner(chunk)
                    
                    # Group results by entity type
                    for entity in results:
                        entity_type = entity.get("entity_group", "")
                        if entity_type in entities:
                            entities[entity_type].append(entity.get("word", ""))
                except Exception as e:
                    print(f"Warning: ContractBERT NER analysis failed for chunk: {e}")
            
            # Try to classify document type
            if contractbert_classifier is not None:
                try:
                    # Use first chunk for document classification
                    doc_type_results = contractbert_classifier(text_chunks[0])
                    if doc_type_results and len(doc_type_results) > 0:
                        doc_type = doc_type_results[0].get("label", "")
                        if doc_type:
                            metadata["document_type"] = doc_type
                except Exception as e:
                    print(f"Warning: ContractBERT classification failed: {e}")
                    
            # Extract dates and find effective date
            dates = entities["DATE"]
            if dates:
                # Look for effective date patterns
                for date in dates:
                    for context in DATE_CONTEXTS:
                        if context in first_page_text.lower() and first_page_text.lower().find(context) + 50 > first_page_text.lower().find(date.lower()):
                            metadata["effective_date"] = date
                            break
                    if metadata["effective_date"]:
                        break
                        
                # If no date found with context, use the first date
                if not metadata["effective_date"] and dates:
                    metadata["effective_date"] = dates[0]
            
            # Use organizations as potential parties
            org_entities = entities["ORG"]
            potential_parties = []
            
            # Filter organizations that look like valid parties
            for org in org_entities:
                org = org.strip()
                if (len(org.split()) > 1 and 
                    (re.search(r"(?:Inc\.|LLC|Ltd\.|Limited|Corp\.|Corporation|B\.V\.|GmbH)", org) or 
                     "company" in org.lower() or 
                     "corporation" in org.lower())):
                    potential_parties.append(org)
            
            # Remove duplicates and false positives
            filtered_parties = []
            for party in potential_parties:
                is_unique = True
                for existing_party in filtered_parties:
                    if party in existing_party or existing_party in party:
                        is_unique = False
                        if len(party) > len(existing_party):
                            filtered_parties.remove(existing_party)
                            filtered_parties.append(party)
                        break
                if is_unique:
                    filtered_parties.append(party)
            
            metadata["parties"] = filtered_parties[:5]  # Limit to 5 most likely parties
        elif nlp is not None:
            # Fall back to SpaCy if ContractBERT isn't available
            doc = nlp(first_page_text[:10000])
            
            # Extract dates using SpaCy
            dates = []
            for ent in doc.ents:
                if ent.label_ == "DATE":
                    dates.append(ent.text)
            
            # Look for effective date patterns
            for date in dates:
                for context in DATE_CONTEXTS:
                    if context in first_page_text.lower() and first_page_text.lower().find(context) + 50 > first_page_text.lower().find(date.lower()):
                        metadata["effective_date"] = date
                        break
                if metadata["effective_date"]:
                    break
                    
            # If no date found with context, use the first date mentioned
            if not metadata["effective_date"] and dates:
                metadata["effective_date"] = dates[0]
            
            # Extract parties using SpaCy
            org_entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
            potential_parties = []
            
            # Filter organizations that look like valid parties
            for org in org_entities:
                org = org.strip()
                if (len(org.split()) > 1 and 
                    (re.search(r"(?:Inc\.|LLC|Ltd\.|Limited|Corp\.|Corporation|B\.V\.|GmbH)", org) or 
                     "company" in org.lower() or 
                     "corporation" in org.lower())):
                    potential_parties.append(org)
            
            # Filter parties
            filtered_parties = []
            for party in potential_parties:
                is_unique = True
                for existing_party in filtered_parties:
                    if party in existing_party or existing_party in party:
                        is_unique = False
                        if len(party) > len(existing_party):
                            filtered_parties.remove(existing_party)
                            filtered_parties.append(party)
                        break
                if is_unique:
                    filtered_parties.append(party)
            
            metadata["parties"] = filtered_parties[:5]  # Limit to 5 most likely parties
        
        # Extract contract title using regex patterns
        for pattern in TITLE_PATTERNS:
            title_match = re.search(pattern, first_page_text, re.IGNORECASE | re.MULTILINE)
            if title_match:
                potential_title = title_match.group(1).strip()
                if len(potential_title.split()) <= 15:
                    metadata["title"] = potential_title
                    break
        
        # If title not found, try to find all-caps sentences
        if not metadata["title"] and nlp is not None:
            doc = nlp(first_page_text[:10000]) if 'doc' not in locals() else doc
            for sent in list(doc.sents)[:3]:
                if sent.text.isupper() and 3 < len(sent.text.split()) < 15:
                    metadata["title"] = sent.text
                    break
        
        # Fallback regex pattern for parties
        if not metadata["parties"]:
            if "Between" in first_page_text:
                try:
                    parties_text = first_page_text.split("Between", 1)[1]
                    if "Effective Date" in parties_text:
                        parties_text = parties_text.split("Effective Date")[0]
                    
                    # Look for party indicators
                    found_parties = []
                    for pattern in PARTY_INDICATORS:
                        matches = re.findall(pattern, parties_text)
                        found_parties.extend([match.strip() for match in matches if match.strip()])
                    
                    if found_parties:
                        metadata["parties"] = found_parties
                except Exception:
                    pass
        
        # If not determined by ContractBERT, infer document type
        if metadata["document_type"] == "Contract":
            doc_text_lower = first_page_text.lower()
            type_scores = {}
            
            # Use the imported DOC_TYPES constant
            for doc_type, keywords in DOC_TYPES.items():
                score = sum(doc_text_lower.count(keyword.lower()) for keyword in keywords)
                type_scores[doc_type] = score
            
            if type_scores:
                best_type = max(type_scores.items(), key=lambda x: x[1])
                if best_type[1] > 0:
                    metadata["document_type"] = best_type[0]
    
    return metadata