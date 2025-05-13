#!/usr/bin/env python3
"""
Articles Extraction Module

This module handles extraction of articles and sections 
from the parsed contract JSON using advanced NLP techniques.
"""

import re
from typing import Dict, List, Any

from contract_constants import (
    ROMAN_TO_NUMBER, ARTICLE_PATTERNS, SECTION_PATTERNS
)


def extract_articles(data: List[Dict[str, Any]], nlp, contractbert_ner) -> List[Dict[str, Any]]:
    """Extract articles and sections using SpaCy and ContractBERT for better structure analysis."""
    articles = []
    
    # Process all pages to extract structure
    for document in data:
        pages_text = []
        for page in document["pages"]:
            pages_text.append(page["text"])
        
        # Combine all text for better pattern matching across page breaks
        full_text = "\n".join(pages_text)
        
        # Process in chunks to avoid memory issues with large documents
        chunk_size = 10000
        text_chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
        
        # Use ContractBERT for structural entity recognition
        print("Using ContractBERT to identify document structure...")
        bert_chunk_size = 450  # Smaller for BERT models
        bert_chunks = [full_text[i:i+bert_chunk_size] for i in range(0, min(len(full_text), 50000), bert_chunk_size)]
        
        # Variables to track document structural elements
        structure_entities = []
        
        for i, chunk in enumerate(bert_chunks):
            # Process each chunk with ContractBERT
            results = contractbert_ner(chunk)
            
            for entity in results:
                # Look for article and section headers
                word = entity.get("word", "")
                entity_group = entity.get("entity_group", "")
                
                # Identify potential article headers by label or patterns
                if (entity_group in ["ORG", "LAW"] and 
                    ("ARTICLE" in word.upper() or 
                     any(re.match(pattern, word, re.IGNORECASE) for pattern in ARTICLE_PATTERNS))):
                    
                    structure_entities.append({"type": "article", "text": word, "chunk_idx": i})
        
        # Process identified structural entities
        for idx, entity in enumerate(structure_entities):
            if entity["type"] == "article":
                # Extract article number and title using regex
                for pattern in ARTICLE_PATTERNS:
                    match = re.search(pattern, entity["text"], re.IGNORECASE)
                    if match:
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
                        break
        
        # If no articles identified through ContractBERT, use SpaCy's linguistic features
        if not articles:
            print("Using SpaCy's linguistic features to identify document structure...")
            for i, chunk in enumerate(text_chunks):
                doc = nlp(chunk)
                
                # Look for sentence patterns that could be article headers
                for sent in doc.sents:
                    # Check for potential headers using linguistic features
                    if (sent.text.isupper() or 
                        re.match(r"ARTICLE|Article|Section|\d+\.\s*[A-Z]", sent.text)):
                        
                        # Extract potential article number and title
                        for pattern in ARTICLE_PATTERNS:
                            match = re.search(pattern, sent.text)
                            if match:
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
                                break
                        
                    # If no specific pattern match but sentence looks like a header
                    if not articles and sent.text.isupper() and len(sent.text.split()) < 8:
                        articles.append({
                            "number": str(len(articles) + 1), 
                            "numeric_id": str(len(articles) + 1), 
                            "title": sent.text.strip(),
                            "content": "",
                            "sections": []
                        })
        
        # Sort articles to ensure proper order
        if articles:
            try:
                articles.sort(key=lambda x: int(x["numeric_id"]))
            except (ValueError, TypeError):
                # If conversion fails, maintain the original order
                pass
        
        # Extract sections within articles
        for idx, article in enumerate(articles):
            # Find the article's position in the text
            article_pattern = f"ARTICLE\\s+{re.escape(article['number'])}|Article\\s+{re.escape(article['number'])}"
            if article['title']:
                article_pattern += f"|{re.escape(article['title'])}"
            
            article_start_idx = -1
            for match in re.finditer(article_pattern, full_text, re.IGNORECASE):
                article_start_idx = match.start()
                break
            
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
                next_art_pattern = f"ARTICLE\\s+{re.escape(articles[idx+1]['number'])}|Article\\s+{re.escape(articles[idx+1]['number'])}|{re.escape(next_art_title)}"
                
                next_match = re.search(next_art_pattern, full_text[article_start_idx:], re.IGNORECASE)
                if next_match:
                    article_end_idx = article_start_idx + next_match.start()
            
            # Extract article text
            if article_start_idx >= 0:
                article_text = full_text[article_start_idx:article_end_idx]
                
                # Use NLP for section identification
                section_chunks = []
                
                # Divide article into manageable chunks for NLP processing
                article_chunk_size = min(len(article_text), 10000)
                article_chunks = [article_text[i:i+article_chunk_size] for i in range(0, len(article_text), article_chunk_size)]
                
                for chunk in article_chunks:
                    doc = nlp(chunk)
                    
                    # Use linguistic features to identify potential section headers
                    for sent in doc.sents:
                        # Look for patterns that suggest a section header
                        if (re.match(r"^\d+\.\d+\s+[A-Z]", sent.text) or  # Like "1.2 Section Title"
                            re.match(r"^[a-z]\)\s+[A-Z]", sent.text)):     # Like "a) Section Title"
                            
                            section_chunks.append(sent.text)
                
                # Process potential section headers
                for section_text in section_chunks:
                    for pattern in SECTION_PATTERNS:
                        match = re.search(pattern, section_text)
                        if match and len(match.groups()) >= 2:
                            section_num = match.group(1)
                            section_title = match.group(2).strip()
                            
                            # Add section to the article
                            section = {
                                "number": section_num,
                                "title": section_title,
                                "content": ""
                            }
                            article["sections"].append(section)
                            break
                
                # If NLP approach didn't find sections, use ContractBERT
                if not article["sections"]:
                    # Process article text with ContractBERT
                    bert_art_chunks = [article_text[i:i+bert_chunk_size] for i in range(0, min(len(article_text), 20000), bert_chunk_size)]
                    
                    for chunk in bert_art_chunks:
                        results = contractbert_ner(chunk)
                        
                        for entity in results:
                            word = entity.get("word", "")
                            
                            # Check if this looks like a section header
                            if re.match(r"\d+\.\d+\s+\w+|\([a-z]\)\s+\w+", word):
                                for pattern in SECTION_PATTERNS:
                                    match = re.search(pattern, word)
                                    if match and len(match.groups()) >= 2:
                                        section_num = match.group(1)
                                        section_title = match.group(2).strip()
                                        
                                        # Add section to article
                                        section = {
                                            "number": section_num,
                                            "title": section_title,
                                            "content": ""
                                        }
                                        
                                        # Check for duplicates
                                        if not any(s["number"] == section_num for s in article["sections"]):
                                            article["sections"].append(section)
                
                # Extract content for each section
                for i, section in enumerate(article["sections"]):
                    section_pattern = f"{re.escape(section['number'])}\\s+{re.escape(section['title'])}"
                    section_match = re.search(section_pattern, article_text)
                    
                    if not section_match:
                        continue
                        
                    section_start = section_match.end()
                    
                    # Find end of this section (start of next section or end of article)
                    section_end = len(article_text)
                    if i < len(article["sections"]) - 1:
                        next_sec = article["sections"][i+1]
                        next_pattern = f"{re.escape(next_sec['number'])}\\s+{re.escape(next_sec['title'])}"
                        next_match = re.search(next_pattern, article_text[section_start:])
                        if next_match:
                            section_end = section_start + next_match.start()
                    
                    # Store section content
                    section_content = article_text[section_start:section_end].strip()
                    section["content"] = section_content
                
                # If no sections were found, store the entire article text as content
                if not article["sections"]:
                    # Remove the article header from the content
                    content_start = 0
                    for pattern in ARTICLE_PATTERNS:
                        header_match = re.search(pattern, article_text)
                        if header_match:
                            content_start = header_match.end()
                            break
                    
                    article["content"] = article_text[content_start:].strip()
    
    return articles