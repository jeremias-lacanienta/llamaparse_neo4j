"""
Extract Module

This package contains the extraction functionality for the LlamaParse to Neo4j converter.
It includes modules for extracting contract metadata, articles, and parties from contract documents,
as well as a TXT fallback parser for when JSON structure is inadequate.
"""

# Use relative imports for internal modules
from .metadata import extract_contract_metadata
from .articles import extract_articles
from .parties import extract_parties
from .txt_parser import (
    read_txt_file, extract_articles_from_text, 
    extract_contract_metadata_from_text
)

__all__ = ["extract_contract_metadata", "extract_articles", "extract_parties"]