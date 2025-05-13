#!/usr/bin/env python3
"""
Parties Extraction Module

This module handles extraction of party information and signatories 
from the parsed contract JSON using advanced NLP techniques.
"""

import re
from typing import Dict, List, Any

from contract_constants import (
    ENTITY_PATTERNS, ORG_TYPES, SIGNATURE_PATTERNS
)


def extract_parties(data: List[Dict[str, Any]], nlp, contractbert_ner) -> List[Dict[str, Any]]:
    """Extract detailed information about the parties using ContractBERT and SpaCy NER."""
    parties = []
    
    if not data or "pages" not in data[0]:
        return parties
    
    # Get text from first few pages where party information is usually found
    pages_to_check = min(3, len(data[0]["pages"]))
    first_pages_text = "\n".join([data[0]["pages"][i]["text"] for i in range(pages_to_check)])
    
    # Get text from last few pages where signatures are usually found
    last_pages_text = ""
    if len(data[0]["pages"]) > 2:
        last_pages = data[0]["pages"][-2:]
        last_pages_text = "\n".join([page["text"] for page in last_pages])
    
    # Process with ContractBERT for primary entity extraction
    print("Using ContractBERT for party detection...")
    
    # Process the text with ContractBERT in chunks
    chunk_size = 450
    first_pages_chunks = [first_pages_text[i:i+chunk_size] for i in range(0, min(len(first_pages_text), 10000), chunk_size)]
    
    # Track identified organizations and persons
    bert_entities = {"ORG": [], "PERSON": []}
    
    for chunk in first_pages_chunks:
        # Process chunk with ContractBERT
        results = contractbert_ner(chunk)
        
        # Extract entities by type
        for entity in results:
            entity_type = entity.get("entity_group", "")
            if entity_type in ["ORG", "PERSON"]:
                word = entity.get("word", "").strip()
                if word and len(word) > 2:  # Filter out very short entities
                    bert_entities[entity_type].append(word)
    
    # Filter out likely parties from the organizations
    potential_parties = []
    
    # Process organization entities from ContractBERT
    for org in bert_entities["ORG"]:
        # Apply heuristics to identify legitimate party names
        if (len(org.split()) > 1 and  # Multi-word names are more likely to be organizations
            any(re.search(pattern, org) for pattern in [
                r"Inc\.|LLC|Ltd\.|Limited|Corp\.|Corporation|B\.V\.|GmbH",
                r"Company|Corporation|Technologies|Systems|International"
            ])):
            potential_parties.append(org)
        
        # Check Organizations Near Party-Indicating Context
        if any(indicator in first_pages_text for indicator in [
            f"party", f"between.*{org}", f"{org}.*agrees", f"{org}.*hereinafter",
            f"{org}.*referred to"
        ]):
            potential_parties.append(org)
    
    # Look specifically near "Between" and "And" for parties
    between_match = re.search(r"Between\s+(.+?)\s+and\s+(.+?)(?=\s+(?:Effective Date|WITNESSETH|WHEREAS|NOW, THEREFORE|$))",
                             first_pages_text, re.IGNORECASE | re.DOTALL)
    
    if between_match:
        party1_text = between_match.group(1).strip()
        party2_text = between_match.group(2).strip()
        
        # Search for organizations in these candidate party texts
        for party_text in [party1_text, party2_text]:
            for org in bert_entities["ORG"]:
                if org in party_text:
                    if org not in potential_parties:
                        potential_parties.append(org)
    
    # Enhance with SpaCy NLP to find additional parties
    print("Enhancing party detection with SpaCy...")
    
    # Process in chunks to handle large documents
    spacy_chunk_size = 10000
    first_pages_chunks = [first_pages_text[i:i+spacy_chunk_size] for i in range(0, len(first_pages_text), spacy_chunk_size)]
    
    for chunk in first_pages_chunks:
        doc = nlp(chunk)
        
        # Extract organization entities
        for ent in doc.ents:
            if ent.label_ == "ORG" and len(ent.text) > 2:
                org = ent.text.strip()
                # Organizations are typically multiword and often include legal suffixes
                if len(org.split()) > 1 and len(org) > 5:
                    if org not in potential_parties:
                        potential_parties.append(org)
        
        # Use noun chunks to find potential missed organizations
        for chunk in doc.noun_chunks:
            # Check if noun chunk contains typical organization words
            if any(org_word in chunk.text.lower() for org_word in [
                "inc", "corp", "llc", "ltd", "company", "corporation",
                "technologies", "systems", "associates", "partners"
            ]):
                org = chunk.text.strip()
                if len(org.split()) > 1 and len(org) > 5 and org not in potential_parties:
                    potential_parties.append(org)
    
    # Create party records for the most likely organizations
    seen_parties = set()
    for party_name in potential_parties:
        # Normalize party name (remove extra spaces, standardize quotes)
        party_name = re.sub(r'\s+', ' ', party_name).strip()
        party_name = party_name.replace('"', '"').replace('"', '"')
        
        # Filter out likely false positives
        if any(x in party_name.lower() for x in [
            "article", "section", "agreement", "contract", "date", 
            "herein", "hereof", "hereto", "effective date"
        ]):
            continue
            
        # Avoid duplicates or very similar names
        is_unique = True
        for seen in seen_parties:
            if party_name in seen or seen in party_name:
                is_unique = False
                break
                
        if is_unique and len(party_name) > 5:
            seen_parties.add(party_name)
            
            # Determine entity type
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
    
    # Process signature sections for signatories
    signature_entities = {"organizations": [], "people": []}
    
    # Use ContractBERT for signature extraction
    sig_chunks = [last_pages_text[i:i+chunk_size] for i in range(0, min(len(last_pages_text), 5000), chunk_size)]
    
    for chunk in sig_chunks:
        results = contractbert_ner(chunk)
        
        for entity in results:
            entity_type = entity.get("entity_group", "")
            word = entity.get("word", "").strip()
            
            if entity_type == "ORG" and word:
                signature_entities["organizations"].append(word)
            elif entity_type == "PERSON" and word:
                signature_entities["people"].append(word)
    
    # Enhance with SpaCy
    sig_chunks = [last_pages_text[i:i+spacy_chunk_size] for i in range(0, len(last_pages_text), spacy_chunk_size)]
    
    for chunk in sig_chunks:
        doc = nlp(chunk)
        for ent in doc.ents:
            if ent.label_ == "ORG" and ent.text not in signature_entities["organizations"]:
                signature_entities["organizations"].append(ent.text)
            elif ent.label_ == "PERSON" and ent.text not in signature_entities["people"]:
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
    
    # Use NLP to match people with organizations based on proximity
    sig_doc = nlp(last_pages_text)
    
    org_spans = [ent for ent in sig_doc.ents if ent.label_ == "ORG"]
    person_spans = [ent for ent in sig_doc.ents if ent.label_ == "PERSON"]
    
    # Match people to nearby organizations
    for person in person_spans:
        closest_org = None
        min_distance = float('inf')
        
        # Find closest organization to this person
        for org in org_spans:
            distance = abs(person.start - org.start)
            if distance < min_distance:
                min_distance = distance
                closest_org = org
        
        # If a close organization found and it matches a party
        if closest_org and min_distance < 50:  # Within ~50 tokens
            for party in parties:
                if closest_org.text in party["name"] or party["name"] in closest_org.text:
                    # Add as signatory if not already present
                    signatory = {"name": person.text, "title": "Signatory"}
                    if signatory not in party["signatories"]:
                        party["signatories"].append(signatory)
    
    # If still no matches, distribute people among parties
    if all(len(party["signatories"]) == 0 for party in parties):
        for i, party in enumerate(parties):
            if i < len(signature_entities["people"]):
                party["signatories"].append({
                    "name": signature_entities["people"][i], 
                    "title": "Signatory"
                })
    
    return parties