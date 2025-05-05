#!/usr/bin/env python3
"""
Articles Extraction Module

This module handles extraction of articles and sections 
from the parsed contract JSON.
"""

import re
from typing import Dict, List, Any

from contract_constants import (
    ROMAN_TO_NUMBER, ARTICLE_PATTERNS, SECTION_PATTERNS
)


def extract_articles(data: List[Dict[str, Any]], nlp=None) -> List[Dict[str, Any]]:
    """Extract articles and sections using SpaCy for better text structure analysis.
    
    Args:
        data: The parsed contract JSON data
        nlp: The SpaCy NLP model (optional)
        
    Returns:
        List of article dictionaries with their sections
    """
    articles = []
    
    # Process all pages to extract structure
    for document in data:
        pages_text = []
        for page in document["pages"]:
            pages_text.append(page["text"])
        
        # Combine all text for better pattern matching across page breaks
        full_text = "\n".join(pages_text)
        
        # Use SpaCy to analyze the document structure
        # Process in chunks to avoid memory issues with large documents
        chunk_size = 10000
        text_chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
        
        # First pass: Identify articles using regex patterns
        for pattern in ARTICLE_PATTERNS:
            article_matches = re.finditer(pattern, full_text, re.MULTILINE)
            for match in article_matches:
                article_num = match.group(1)
                article_title = match.group(2).strip() if len(match.groups()) > 1 else "UNTITLED"
                
                # Convert Roman numerals to numeric if needed
                numeric_id = ROMAN_TO_NUMBER.get(article_num.upper(), article_num)
                
                new_article = {
                    "number": article_num,
                    "numeric_id": numeric_id,
                    "title": article_title,
                    "content": "",
                    "sections": []
                }
                articles.append(new_article)
        
        # If no articles found, try using SpaCy to identify document structure
        if not articles and nlp:
            for i, chunk in enumerate(text_chunks):
                doc = nlp(chunk)
                
                # Look for sentence patterns that could be article headers
                for sent in doc.sents:
                    # Check for all-caps sentences that could be headers
                    if sent.text.isupper() and len(sent.text.split()) < 8:
                        articles.append({"number": str(len(articles) + 1), "numeric_id": str(len(articles) + 1), 
                                        "title": sent.text.strip(), "content": "", "sections": []})
        
        # If still no structure found, create a default article
        if not articles:
            articles.append({"number": "1", "numeric_id": "1", "title": "CONTRACT TEXT", 
                            "content": "", "sections": []})
            
        # Sort articles to ensure proper order
        if articles:
            try:
                articles.sort(key=lambda x: int(x["numeric_id"]))
            except (ValueError, TypeError):
                # If conversion fails, maintain the original order
                pass
        
        # Second pass: Identify sections within articles
        for idx, article in enumerate(articles):
            article_start_idx = full_text.find(f"ARTICLE {article['number']}")
            if (article_start_idx == -1):  # Try different formats
                article_start_idx = full_text.find(f"Article {article['number']}")
            
            # If still not found, look for the title itself
            if article_start_idx == -1 and len(article['title']) > 3:
                article_start_idx = full_text.find(article['title'])
            
            # If we can't find the article, use a rough position based on the articles array
            if article_start_idx == -1:
                if idx == 0:
                    article_start_idx = 0
                else:
                    prev_art_title = articles[idx-1]['title']
                    article_start_idx = full_text.find(prev_art_title)
                    if article_start_idx > 0:
                        article_start_idx += len(prev_art_title)
            
            # Determine article end
            article_end_idx = len(full_text)
            if idx < len(articles) - 1:
                next_art_title = articles[idx+1]['title']
                next_art_idx = full_text.find(next_art_title, article_start_idx)
                if next_art_idx > 0:
                    article_end_idx = next_art_idx
            
            # Extract article content
            if article_start_idx >= 0:
                article_text = full_text[article_start_idx:article_end_idx]
                
                # Process this article's text with SpaCy for better section identification
                article_chunks = [article_text[i:i+chunk_size] for i in range(0, len(article_text), chunk_size)]
                
                # Look for sections using regex patterns
                for pattern in SECTION_PATTERNS:
                    section_matches = re.finditer(pattern, article_text, re.MULTILINE)
                    for match in section_matches:
                        section_num = match.group(1)
                        section_title = match.group(2).strip()
                        
                        # Add section to article
                        section = {
                            "number": section_num,
                            "title": section_title,
                            "content": ""
                        }
                        article["sections"].append(section)
                
                # Find content for each section
                for i, section in enumerate(article["sections"]):
                    section_start = article_text.find(f"{section['number']} {section['title']}")
                    if section_start == -1:
                        continue
                        
                    section_start += len(f"{section['number']} {section['title']}")
                    
                    # Find end of this section (start of next section or end of article)
                    section_end = article_end_idx - article_start_idx
                    if i < len(article["sections"]) - 1:
                        next_sec = article["sections"][i+1]
                        next_start = article_text.find(f"{next_sec['number']} {next_sec['title']}")
                        if next_start > 0:
                            section_end = next_start
                    
                    # Store section content
                    section_content = article_text[section_start:section_end].strip()
                    section["content"] = section_content
    
    return articles