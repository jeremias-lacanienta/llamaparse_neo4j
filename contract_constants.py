#!/usr/bin/env python3
"""
Contract Constants and Pattern Definitions

This module contains constants and pattern definitions used in legal document processing,
including regex patterns, spaCy matcher patterns, and various mappings used for
contract analysis.
"""

# Mapping for numeric to Roman numerals for article identification
ROMAN_TO_NUMBER = {
    "I": "1", "II": "2", "III": "3", "IV": "4", "V": "5",
    "VI": "6", "VII": "7", "VIII": "8", "IX": "9", "X": "10",
    "XI": "11", "XII": "12", "XIII": "13", "XIV": "14", "XV": "15",
    "XVI": "16", "XVII": "17", "XVIII": "18", "XIX": "19", "XX": "20",
}

# Regex patterns for recognizing article headers and sections
ARTICLE_PATTERNS = [
    r"ARTICLE\s+([IVXivx]+)\s*[-–—.:]\s*(.*?)(?=$|\n)",
    r"ARTICLE\s+(\d+)\s*[-–—.:]\s*(.*?)(?=$|\n)",
    r"(\d+)\.\s*([A-Z][A-Za-z\s]+)(?=$|\n)",
    r"([A-Z][A-Za-z\s]+)\s*\n",
    r"SECTION\s+(\d+)[.:]\s*(.*?)(?=$|\n)"
]

# Regex patterns for sections
SECTION_PATTERNS = [
    r"(\d+\.\d+)\s+(.*?)(?=$|\n)",
    r"(\d+\.\d+\.\d+)\s+(.*?)(?=$|\n)",
    r"(\d+\.\d+[a-z])\s+(.*?)(?=$|\n)",
    r"([A-Za-z])\.\s+(.*?)(?=$|\n)",
    r"\(([a-z])\)\s+(.*?)(?=$|\n)"
]

# spaCy matcher patterns for definitions
DEFINITION_PATTERNS = [
    [{"LOWER": {"IN": ["means", "shall", "will"]}}, {"LOWER": "mean"}, {"LOWER": "the"}],
    [{"LOWER": {"IN": ["means", "shall", "will"]}}, {"LOWER": "refer"}, {"LOWER": "to"}],
    [{"LOWER": "is"}, {"LOWER": "defined"}, {"LOWER": "as"}],
    [{"LOWER": "shall"}, {"LOWER": "have"}, {"LOWER": "the"}, {"LOWER": "meaning"}]
]

# spaCy matcher patterns for obligation identification
OBLIGATION_PATTERNS = [
    [{"LOWER": {"IN": ["shall", "must", "will"]}}, {"POS": "VERB"}],
    [{"LOWER": "is"}, {"LOWER": {"IN": ["required", "obligated"]}}, {"LOWER": "to"}],
    [{"LOWER": "has"}, {"LOWER": "a"}, {"LOWER": {"IN": ["duty", "obligation"]}}, {"LOWER": "to"}]
]

# spaCy matcher patterns for condition identification
CONDITION_PATTERNS = [
    [{"LOWER": {"IN": ["if", "when", "whenever"]}}, {"OP": "*"}],
    [{"LOWER": "in"}, {"LOWER": "the"}, {"LOWER": "event"}, {"LOWER": "that"}],
    [{"LOWER": "subject"}, {"LOWER": "to"}],
    [{"LOWER": "provided"}, {"LOWER": "that"}],
    [{"LOWER": "on"}, {"LOWER": "condition"}, {"LOWER": "that"}]
]

# spaCy matcher patterns for term identification
TERM_PATTERNS = [
    [{"LOWER": "term"}, {"IS_PUNCT": True}, {"LOWER": "the"}],
    [{"LOWER": {"IN": ["during", "throughout"]}}, {"LOWER": "the"}, {"LOWER": "term"}],
    [{"LOWER": "expiration"}, {"LOWER": "date"}]
]

# spaCy matcher patterns for payment clauses
PAYMENT_PATTERNS = [
    [{"LOWER": {"IN": ["payment", "fee", "compensation", "price"]}}, {"OP": "*"}],
    [{"LOWER": {"IN": ["pay", "reimburse", "compensate"]}}, {"POS": "DET"}, {"OP": "*"}]
]

# Regex patterns for contract title extraction
TITLE_PATTERNS = [
    r"(.*?(?:AGREEMENT|CONTRACT))",  # Standard AGREEMENT/CONTRACT endings
    r"(^.+?(?=Between|BETWEEN|between))",  # Text before "Between"
    r"(^[A-Z\s]+(?:\s*[-–—]\s*[A-Z\s]+)?)"  # All-caps text possibly with a dash
]

# Document type classification patterns
DOC_TYPES = {
    "Non-Disclosure Agreement": ["confidential", "disclose", "NDA", "non-disclosure"],
    "Employment Contract": ["employ", "salary", "position", "hire", "job", "work"],
    "Lease Agreement": ["lease", "rent", "landlord", "tenant", "property"],
    "License Agreement": ["license", "royalty", "intellectual property", "patent"],
    "Services Agreement": ["service", "perform", "deliverable"],
    "Purchase Agreement": ["purchase", "buy", "acquire", "sale"],
    "Merger Agreement": ["merger", "acquire", "acquisition", "combine"]
}

# Date context patterns for effective date identification
DATE_CONTEXTS = [
    "effective date",
    "dated as of",
    "agreement date",
    "executed on",
    "entered into on"
]

# Entity patterns for party extraction
ENTITY_PATTERNS = [
    # Name + entity type in parentheses
    r"([A-Za-z0-9\s,\.&]+)(?:\((?:a|an)\s+([^)]+)\))",
    # Name + Inc./LLC/Ltd./Corp./etc.
    r"([A-Za-z0-9\s,\.&]+(?:Inc\.|LLC|Ltd\.|Limited|Corp\.|Corporation|B\.V\.|GmbH|S\.A\.|S\.p\.A\.))\s*(?:\([^)]*\))?",
    # Name followed by jurisdiction indicator
    r"([A-Za-z0-9\s,\.&]+),\s*(?:a|an)\s+([A-Za-z\s]+(?:corporation|company|partnership|entity|organization))"
]

# Organization types for entity classification
ORG_TYPES = [
    (r"Inc\.|Corporation|Corp\.", "Corporation"),
    (r"LLC", "Limited Liability Company"),
    (r"Ltd\.|Limited", "Limited Company"),
    (r"B\.V\.", "Dutch Private Limited Company"),
    (r"GmbH", "German Limited Liability Company"),
    (r"S\.A\.", "Anonymous Society"),
    (r"LLP", "Limited Liability Partnership"),
    (r"AG", "German Public Company"),
    (r"ApS", "Danish Private Limited Company"),
    (r"OY|OYJ", "Finnish Company"),
    (r"PLC|P\.L\.C\.", "Public Limited Company")
]

# Signature patterns for extracting signatories
SIGNATURE_PATTERNS = [
    r"(?:For|By):\s*([A-Za-z0-9\s,\.&]+)\s*[_\s-]*\s*(?:Name|Signature):\s*([A-Za-z\s\.-]+)\s*(?:Title|Position):\s*([A-Za-z\s\.-]+)",
    r"([A-Za-z0-9\s,\.&]+)\s*\n\s*By:\s*[_\s-]*\s*\n\s*Name:\s*([A-Za-z\s\.-]+)\s*\n\s*Title:\s*([A-Za-z\s\.-]+)"
]

# Party indicators for regex extraction
PARTY_INDICATORS = [
    r"([A-Za-z0-9\s,\.]+?(?:Inc\.|LLC|Ltd\.|Limited|Corp\.|Corporation|B\.V\.|GmbH|S\.A\.|S\.p\.A\.))",
    r"([A-Za-z0-9\s,\.]+?(?:\(\".*?\"\)))",  # Company name followed by defined term in quotes
    r"([A-Za-z0-9\s,\.]+?(?:\([A-Za-z0-9\s,\.]+?\)))"  # Company name followed by jurisdiction in parentheses
]