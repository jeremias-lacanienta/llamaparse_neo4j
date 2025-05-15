#!/usr/bin/env python3
"""
TXT Parser Module

This module provides fallback functionality to extract contract information from TXT files
when JSON structure has issues or lacks certain key information.
"""

import re
import os
from typing import Dict, List, Any, Optional

from contract_constants import (
    ARTICLE_PATTERNS, SECTION_PATTERNS, ROMAN_TO_NUMBER
)

def read_txt_file(txt_file_path: str) -> str:
    """Read content from a text file."""
    if not os.path.exists(txt_file_path):
        raise FileNotFoundError(f"TXT file not found: {txt_file_path}")
    
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_articles_from_text(text: str) -> List[Dict[str, Any]]:
    """Extract articles from plain text using regex patterns."""
    articles = []
    
    # Find all article headers in the document
    article_matches = []
    for pattern in ARTICLE_PATTERNS:
        for match in re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE):
            article_num = match.group(1)
            article_title = match.group(2).strip() if len(match.groups()) > 1 else "UNTITLED"
            article_matches.append({
                "number": article_num,
                "title": article_title,
                "start": match.start(),
                "end": match.end()
            })
    
    # Sort matches by their position in the text
    article_matches.sort(key=lambda x: x["start"])
    
    # Process each article
    for i, match in enumerate(article_matches):
        article_num = match["number"]
        article_title = match["title"]
        
        # Convert Roman numerals to numeric if needed
        numeric_id = ROMAN_TO_NUMBER.get(article_num.upper(), article_num)
        
        # Determine where this article ends (start of next article or end of text)
        article_start = match["end"]
        article_end = len(text)
        if i < len(article_matches) - 1:
            article_end = article_matches[i + 1]["start"]
        
        # Extract article content
        article_content = text[article_start:article_end].strip()
        
        # Create article object
        article = {
            "number": article_num,
            "numeric_id": numeric_id,
            "title": article_title,
            "content": article_content,
            "sections": []
        }
        
        # Extract sections within this article
        extract_sections_from_text(article, article_content)
        
        articles.append(article)
    
    return articles

def extract_sections_from_text(article: Dict[str, Any], article_text: str) -> None:
    """Extract sections from article text and add them to the article dictionary."""
    section_matches = []
    for pattern in SECTION_PATTERNS:
        for match in re.finditer(pattern, article_text, re.MULTILINE):
            section_num = match.group(1)
            section_title = match.group(2).strip() if len(match.groups()) > 1 else "UNTITLED"
            section_matches.append({
                "number": section_num,
                "title": section_title,
                "start": match.start(),
                "end": match.end()
            })
    
    # Sort sections by their position in the text
    section_matches.sort(key=lambda x: x["start"])
    
    # Process each section
    for i, match in enumerate(section_matches):
        section_num = match["number"]
        section_title = match["title"]
        
        # Determine section content boundaries
        section_start = match["end"]
        section_end = len(article_text)
        if i < len(section_matches) - 1:
            section_end = section_matches[i + 1]["start"]
        
        # Extract section content
        section_content = article_text[section_start:section_end].strip()
        
        # Add section to article
        section = {
            "number": section_num,
            "title": section_title,
            "content": section_content
        }
        article["sections"].append(section)

def extract_contract_metadata_from_text(text: str) -> Dict[str, Any]:
    """Extract basic contract metadata from text."""
    metadata = {
        "title": "Untitled Contract",  # Add default title 
        "document_type": "Unknown",
        "execution_date": "",
        "effective_date": "",
        "parties": []
    }
    
    # Try to identify document type
    if re.search(r"(?i)\bagreement\b", text[:1000]):
        metadata["document_type"] = "Agreement"
    elif re.search(r"(?i)\bcontract\b", text[:1000]):
        metadata["document_type"] = "Contract"
    elif re.search(r"(?i)\bamendment\b", text[:1000]):
        metadata["document_type"] = "Amendment"
    elif re.search(r"(?i)\baddendum\b", text[:1000]):
        metadata["document_type"] = "Addendum"
    
    # Try to extract title from first few lines
    lines = text.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    # Extract title using multiple techniques for robustness
    potential_titles = []
    
    # Method 1: Look for ALL CAPS lines that could be titles
    if non_empty_lines:
        for i, line in enumerate(non_empty_lines[:10]):  # Check first 10 non-empty lines
            # Strong title indicators: all caps + "AGREEMENT"/"CONTRACT"/"LICENSE"
            if line.isupper() and len(line.split()) >= 2 and len(line.split()) <= 15:
                if any(keyword in line for keyword in ["AGREEMENT", "CONTRACT", "LICENSE", "LEASE"]):
                    potential_titles.append((line, 10))  # High confidence score
                else:
                    potential_titles.append((line, 5))   # Medium confidence
            # Mixed case but has agreement keywords
            elif any(keyword in line.upper() for keyword in ["AGREEMENT", "CONTRACT", "LICENSE"]):
                potential_titles.append((line, 8))
                
    # Method 2: Look for lines containing typical agreement/contract terms
    agreement_types = ["service", "employment", "non-disclosure", "confidentiality", 
                      "sale", "purchase", "master", "subscription", "consulting", 
                      "license", "partnership", "distribution", "supply"]
    
    for i, line in enumerate(non_empty_lines[:15]):  # Check more lines for this method
        line_lower = line.lower()
        if any(f"{term} agreement" in line_lower for term in agreement_types):
            potential_titles.append((line, 9))
        elif "agreement" in line_lower and len(line.split()) <= 10:
            potential_titles.append((line, 7))
                
    # Select the best title based on confidence score
    if potential_titles:
        best_title = max(potential_titles, key=lambda x: x[1])[0]
        metadata["title"] = best_title
    # If no title found with confidence, use the first non-empty line as last resort
    elif non_empty_lines:
        metadata["title"] = non_empty_lines[0]

    # Try to extract dates
    # Effective date pattern
    effective_date_match = re.search(
        r"(?i)effective\s+(?:as\s+of\s+)?(?:date|:)?\s*[:;]?\s*(\w+\s+\d{1,2}(?:st|nd|rd|th)?[\s,]+\d{4}|\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4})",
        text
    )
    if effective_date_match:
        metadata["effective_date"] = effective_date_match.group(1).strip()
    
    # Execution date patterns
    execution_date_match = re.search(
        r"(?i)(?:executed|signed|dated)(?:\s+as\s+of)?\s+(?:this)?\s*(\w+\s+\d{1,2}(?:st|nd|rd|th)?[\s,]+\d{4}|\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4})",
        text
    )
    if execution_date_match:
        metadata["execution_date"] = execution_date_match.group(1).strip()
        
    # Try to extract parties
    # This is a simplified approach - might need improvement for complex documents
    party_matches = re.finditer(
        r"(?i)((?:between|by and between|among)\s+)((?:[A-Z][A-Za-z\s,.']*(?:Inc\.|LLC|Ltd\.?|Corporation|Company|Co\.|LP|LLP|Trust|Association)){1,3})",
        text[:3000]
    )
    
    parties = []
    for match in party_matches:
        party_text = match.group(2).strip()
        if party_text and len(party_text) > 3:  # Simple validation
            parties.append({"name": party_text})
    
    metadata["parties"] = parties
    return metadata
