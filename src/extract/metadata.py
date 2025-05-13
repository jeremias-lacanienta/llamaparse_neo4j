#!/usr/bin/env python3
"""
Metadata Extraction Module

This module handles extraction of contract metadata like titles, dates,
document types, and parties from the parsed contract JSON using advanced NLP techniques.
"""

import re
from typing import Dict, List, Any

from contract_constants import (
    TITLE_PATTERNS, DOC_TYPES, DATE_CONTEXTS, PARTY_INDICATORS, DATE_PATTERNS
)


def extract_contract_metadata(data: List[Dict[str, Any]], nlp, 
                             contractbert_ner, contractbert_classifier) -> Dict[str, Any]:
    """Extract key metadata about the contract using ContractBERT and SpaCy NLP."""
    metadata = {"title": "", "effective_date": "", "parties": [], "document_type": "Contract"}
    
    # Check for document metadata in the first page
    if data and len(data) > 0 and "pages" in data[0]:
        first_page_text = data[0]["pages"][0]["text"]
        
        # First, try a direct pattern match for "Effective Date: <date>" format
        effective_date_match = re.search(r"Effective\s+Date:\s*([A-Za-z]+\s+\d{1,2},\s*\d{4})", first_page_text)
        if effective_date_match:
            metadata["effective_date"] = effective_date_match.group(1).strip()
        
        # Use ContractBERT for document classification
        print("Classifying document type with ContractBERT...")
        # Prepare text for classification (first 1000 chars is usually sufficient)
        classification_text = first_page_text[:1000]
        
        # Apply the classifier
        doc_classification = contractbert_classifier(classification_text)
        
        if doc_classification and len(doc_classification) > 0:
            label = doc_classification[0].get("label", "")
            score = doc_classification[0].get("score", 0)
            
            # Only use classification if confidence is reasonable
            if score > 0.7 and label:
                # Map BERT labels to human-readable document types
                label_mapping = {
                    "LABEL_0": "Contract Agreement",
                    "LABEL_1": "License Agreement",
                    "LABEL_2": "Service Agreement",
                    "LABEL_3": "Employment Agreement",
                    "LABEL_4": "Non-Disclosure Agreement",
                    "LABEL_5": "Sales Agreement",
                    "LABEL_6": "Lease Agreement",
                    "LABEL_7": "Financial Agreement"
                }
                
                mapped_type = label_mapping.get(label, label)
                metadata["document_type"] = mapped_type
                print(f"Document classified as: {mapped_type} (score: {score:.2f})")
        
        # Process with ContractBERT NER for entity extraction
        print("Analyzing contract with ContractBERT...")
        # Process the text with ContractBERT in chunks
        chunk_size = 450  # Leave buffer for special tokens
        text_chunks = [first_page_text[i:i+chunk_size] for i in range(0, min(len(first_page_text), 10000), chunk_size)]
        
        # Extract entities using ContractBERT
        entities = {"DATE": [], "ORG": [], "PERSON": [], "MONEY": [], "TIME": [], "LOC": []}
        
        for chunk in text_chunks:
            # Apply NER pipeline to each chunk
            results = contractbert_ner(chunk)
            
            # Group results by entity type
            for entity in results:
                entity_type = entity.get("entity_group", "")
                word = entity.get("word", "").strip()
                if entity_type in entities and word and len(word) > 1:
                    # Try to merge consecutive entities of the same type
                    if (entity_type == "DATE" and entities[entity_type] and 
                        any(date_word.startswith(word) or word.startswith(date_word) 
                            for date_word in entities[entity_type][-3:])):
                        continue  # Skip potential fragments of already identified dates
                        
                    entities[entity_type].append(word)
        
        # Only continue with date extraction if we haven't found it directly
        if not metadata["effective_date"]:
            # Enhance date recognition by matching date patterns in the text
            all_potential_dates = []
            
            # First, use the dates identified by ContractBERT
            all_potential_dates.extend(entities["DATE"])
            
            # Then, try to find additional dates using regex patterns
            for pattern in DATE_PATTERNS:
                for match in re.finditer(pattern, first_page_text):
                    date_str = match.group(0)
                    if date_str not in all_potential_dates:
                        all_potential_dates.append(date_str)
            
            # Look for effective date by proximity to context words
            found_effective_date = False
            for context in DATE_CONTEXTS:
                # Normalize the text by removing punctuation for comparison
                normalized_text = re.sub(r'[.:,;]', ' ', first_page_text.lower())
                context_pos = normalized_text.find(context)
                
                if context_pos >= 0:
                    # Try to find closest date to this context
                    closest_date = None
                    min_distance = float('inf')
                    
                    for date in all_potential_dates:
                        date_lower = date.lower()
                        date_pos = normalized_text.find(date_lower)
                        
                        # Only consider dates that appear after the context within a reasonable distance
                        if date_pos > context_pos and date_pos - context_pos < 100:
                            distance = date_pos - context_pos
                            if distance < min_distance:
                                min_distance = distance
                                closest_date = date
                    
                    if closest_date:
                        metadata["effective_date"] = closest_date
                        found_effective_date = True
                        break
            
            # If no effective date found through context, try dates with specific formatting
            if not found_effective_date:
                # Look for properly formatted dates (Month DD, YYYY)
                month_day_year = re.search(r"([A-Z][a-z]+\s+\d{1,2},\s*\d{4})", first_page_text)
                if month_day_year:
                    metadata["effective_date"] = month_day_year.group(1)
                # If still not found, use the first date from ContractBERT's identified dates
                elif entities["DATE"]:
                    metadata["effective_date"] = entities["DATE"][0]
        
        # Process organizations to identify parties
        org_entities = entities["ORG"]
        potential_parties = []
        
        # Filter organizations that look like valid parties
        for org in org_entities:
            if (len(org.split()) > 1 and  # Multi-word names are more likely to be organizations
                (re.search(r"(?:Inc\.|LLC|Ltd\.|Limited|Corp\.|Corporation|B\.V\.|GmbH)", org) or 
                 any(term in org.lower() for term in ["company", "corporation", "technologies", "systems"]))):
                potential_parties.append(org)
        
        # Remove duplicates and false positives
        filtered_parties = []
        for party in potential_parties:
            # Skip common false positives
            if any(term in party.lower() for term in ["article", "section", "this agreement", "hereinafter"]):
                continue
                
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
        
        # Use SpaCy for title extraction and additional entity analysis
        print("Using SpaCy for document analysis...")
        # Process text with SpaCy, limiting to manageable chunks
        doc = nlp(first_page_text[:min(len(first_page_text), 15000)])
        
        # Extract title if not found by ContractBERT
        if not metadata["title"]:
            # Look for potential title sentences
            title_candidates = []
            for sent in list(doc.sents)[:5]:  # Check first few sentences
                # Title candidates: all caps, contains "AGREEMENT", or has special formatting
                if (sent.text.isupper() and len(sent.text.split()) >= 3 and len(sent.text.split()) <= 15) or \
                   ("AGREEMENT" in sent.text or "CONTRACT" in sent.text):
                    title_candidates.append(sent.text.strip())
            
            # Select the best candidate based on length and keywords
            if title_candidates:
                best_title = title_candidates[0]
                for candidate in title_candidates[1:]:
                    if ("AGREEMENT" in candidate or "CONTRACT" in candidate) and len(candidate.split()) < 15:
                        best_title = candidate
                
                metadata["title"] = best_title
            # If no title found through NLP, try regex patterns
            else:
                for pattern in TITLE_PATTERNS:
                    title_match = re.search(pattern, first_page_text, re.IGNORECASE | re.MULTILINE)
                    if title_match:
                        potential_title = title_match.group(1).strip()
                        if len(potential_title.split()) <= 15:
                            metadata["title"] = potential_title
                            break
        
        # Get additional party information if needed
        if not metadata["parties"]:
            # Get between/and structure parties
            between_match = re.search(r"Between\s+(.+?)\s+and\s+(.+?)(?=\s+(?:Effective Date|WITNESSETH|WHEREAS|NOW, THEREFORE|$))",
                                     first_page_text, re.IGNORECASE | re.DOTALL)
            
            if between_match:
                party1_text = between_match.group(1).strip()
                party2_text = between_match.group(2).strip()
                
                # Process each party text with SpaCy
                for party_text in [party1_text, party2_text]:
                    party_doc = nlp(party_text)
                    
                    # Look for organization entities
                    org_ents = [ent.text for ent in party_doc.ents if ent.label_ == "ORG"]
                    
                    if org_ents:
                        for org in org_ents:
                            if len(org.split()) > 1 and len(org) > 5:
                                # Determine entity type
                                entity_type = "Organization"
                                
                                # Check against organization type patterns
                                for pattern, type_name in DOC_TYPES.items():
                                    if re.search(pattern, org):
                                        entity_type = type_name
                                        break
                                
                                metadata["parties"].append({
                                    "name": org.strip(),
                                    "type": entity_type
                                })
                    else:
                        # If no organization entity found, use the entire party text
                        if len(party_text.split()) > 1 and len(party_text) > 5:
                            metadata["parties"].append({
                                "name": party_text.strip(),
                                "type": "Organization"
                            })
    
    return metadata