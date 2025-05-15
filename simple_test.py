#!/usr/bin/env python3
"""
Simple Title Extraction Test

Tests the title extraction logic directly without importing modules.
"""

import re

def test_title_extraction():
    """Test the title extraction logic directly"""
    # Sample contract text snippets with different title formats
    test_cases = [
        ("""JOINT TECHNOLOGY DEVELOPMENT AND LICENSING AGREEMENT
        Between OmniSynapse Technologies, Inc. and NeuroCore International B.V.
        Effective Date: April 29, 2025""", 
        "JOINT TECHNOLOGY DEVELOPMENT AND LICENSING AGREEMENT"),
        
        ("""Service Agreement
        
        This AGREEMENT is made on January 15, 2025
        Between Company A and Company B""",
        "Service Agreement"),
        
        ("""CONTRACT FOR SOFTWARE DEVELOPMENT SERVICES
        
        This Contract is made and entered into on May 1, 2025""",
        "CONTRACT FOR SOFTWARE DEVELOPMENT SERVICES"),
        
        ("""Simple text document with no clear title.
        Just some paragraphs of information.
        Nothing that looks like a standard contract.""",
        "Nothing that looks like a standard contract."),
        
        ("""Terms and Conditions
        
        These terms govern your use of our services.""",
        "Terms and Conditions"),
    ]
    
    print("Testing title extraction logic...")
    for i, (test_text, expected_title) in enumerate(test_cases):
        # Extract title using our improved algorithm
        metadata = {"title": "Untitled Contract"}
        
        # Simulate our extraction algorithm
        lines = test_text.split('\n')
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
        
        actual_title = metadata.get("title", "")
        
        print(f"Test case {i+1}: ", end="")
        if actual_title == expected_title:
            print(f"✓ PASS - Title correctly extracted: '{actual_title}'")
        else:
            print(f"✗ FAIL - Expected: '{expected_title}', Got: '{actual_title}'")

if __name__ == "__main__":
    test_title_extraction()
    print("\nTitle extraction testing complete!")
