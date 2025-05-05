#!/usr/bin/env python3
"""
Parties Extraction Module

This module handles extraction of party information and signatories 
from the parsed contract JSON.
"""

import re
from typing import Dict, List, Any

from contract_constants import (
    ENTITY_PATTERNS, ORG_TYPES, SIGNATURE_PATTERNS
)


def extract_parties(data: List[Dict[str, Any]], nlp=None) -> List[Dict[str, Any]]:
    """Extract detailed information about the parties using SpaCy NER.
    
    Args:
        data: The parsed contract JSON data
        nlp: The SpaCy NLP model (optional)
        
    Returns:
        List of party dictionaries with their information
    """
    parties = []
    
    if not data or "pages" not in data[0] or not nlp:
        return parties
    
    # Get text from first few pages where party information is usually found
    pages_to_check = min(3, len(data[0]["pages"]))
    first_pages_text = "\n".join([data[0]["pages"][i]["text"] for i in range(pages_to_check)])
    
    # Get text from last few pages where signatures are usually found
    last_pages_text = ""
    if len(data[0]["pages"]) > 2:
        last_pages = data[0]["pages"][-2:]
        last_pages_text = "\n".join([page["text"] for page in last_pages])
    
    # Process the text with SpaCy for entity extraction
    # Process in chunks to handle large documents
    chunk_size = 10000
    first_pages_chunks = [first_pages_text[i:i+chunk_size] for i in range(0, len(first_pages_text), chunk_size)]
    
    org_entities = []
    person_entities = []
    
    # Process each chunk with SpaCy
    for chunk in first_pages_chunks:
        doc = nlp(chunk)
        
        # Extract organization and person entities
        for ent in doc.ents:
            if ent.label_ == "ORG":
                org_entities.append(ent.text)
            elif ent.label_ == "PERSON":
                person_entities.append(ent.text)
    
    # Filter organization entities to find likely parties
    potential_parties = []
    for org in org_entities:
        org = org.strip()
        # Organizations are typically multiword and often include legal suffixes
        if len(org.split()) > 1 and len(org) > 5:
            potential_parties.append(org)
    
    # If SpaCy NER didn't find clear parties, try the Between/And structure
    if len(potential_parties) < 2:
        between_and_pattern = r"Between\s+(?:.*?)\s+and\s+(?:.*?)(?:Effective Date|WITNESSETH|WHEREAS|NOW, THEREFORE|$)"
        between_match = re.search(between_and_pattern, first_pages_text, re.DOTALL | re.IGNORECASE)
        
        if between_match:
            between_text = between_match.group(0)
            
            # Split on "and" to get individual parties (only the most significant "and")
            party_texts = re.split(r"\s+and\s+", between_text, maxsplit=1)
            
            # Process each party text
            for party_text in party_texts:
                # Ignore the "Between" in the first part
                party_text = re.sub(r"^Between\s+", "", party_text, flags=re.IGNORECASE)
                
                # Try to extract party name and entity type
                for pattern in ENTITY_PATTERNS:
                    match = re.search(pattern, party_text.strip(), re.IGNORECASE)
                    if match:
                        name = match.group(1).strip()
                        entity_type = match.group(2).strip() if len(match.groups()) > 1 else "Organization"
                        
                        potential_parties.append(name)
                        break
    
    # Create party records for the most likely organizations
    seen_parties = set()
    for party_name in potential_parties:
        # Avoid duplicates or very similar names
        is_unique = True
        for seen in seen_parties:
            if party_name in seen or seen in party_name:
                is_unique = False
                break
                
        if is_unique and len(party_name) > 5:
            seen_parties.add(party_name)
            
            # Try to determine entity type
            entity_type = "Organization"
            
            # Check against organization type patterns
            for pattern, type_name in ORG_TYPES:
                if re.search(pattern, party_name):
                    entity_type = type_name
                    break
            
            parties.append({
                "name": party_name,
                "type": entity_type,
                "signatories": []
            })
    
    # Process signature sections to find signatories
    sig_chunks = [last_pages_text[i:i+chunk_size] for i in range(0, len(last_pages_text), chunk_size)]
    
    # Use SpaCy to identify people and organizations in signature blocks
    signature_entities = {"organizations": [], "people": []}
    
    for chunk in sig_chunks:
        doc = nlp(chunk)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                signature_entities["organizations"].append(ent.text)
            elif ent.label_ == "PERSON":
                signature_entities["people"].append(ent.text)
    
    # Match signature patterns to extract signatories and their roles
    for pattern in SIGNATURE_PATTERNS:
        matches = re.finditer(pattern, last_pages_text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            if len(match.groups()) >= 3:
                company_name = match.group(1).strip()
                person_name = match.group(2).strip()
                title = match.group(3).strip()
                
                # Find matching party
                for party in parties:
                    # Check if this signatory belongs to this party
                    if company_name in party["name"] or party["name"] in company_name:
                        party["signatories"].append({"name": person_name, "title": title})
                        break
    
    # If no signature matches found, try to assign persons from SpaCy NER to parties
    if all(len(party["signatories"]) == 0 for party in parties) and signature_entities["people"]:
        # Try to distribute the identified people among parties
        for i, party in enumerate(parties):
            if i < len(signature_entities["people"]):
                party["signatories"].append({"name": signature_entities["people"][i], 
                                           "title": "Signatory"})
    
    return parties