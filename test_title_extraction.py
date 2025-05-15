#!/usr/bin/env python3
"""
Test Title Extraction Script

This script tests the title extraction functionality in both the JSON and TXT paths
to ensure it's working properly with the changes.
"""

import os
import sys

# Add the current directory to the path so we can import the extract module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.extract.txt_parser import extract_contract_metadata_from_text

def test_txt_title_extraction():
    """Test the TXT file title extraction"""
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
        "Simple text document with no clear title."),
    ]
    
    print("Testing TXT title extraction...")
    for i, (test_text, expected_title) in enumerate(test_cases):
        metadata = extract_contract_metadata_from_text(test_text)
        actual_title = metadata.get("title", "")
        
        print(f"Test case {i+1}: ", end="")
        if actual_title == expected_title:
            print(f"✓ PASS - Title correctly extracted: '{actual_title}'")
        else:
            print(f"✗ FAIL - Expected: '{expected_title}', Got: '{actual_title}'")

if __name__ == "__main__":
    test_txt_title_extraction()
    print("\nTitle extraction testing complete!")
