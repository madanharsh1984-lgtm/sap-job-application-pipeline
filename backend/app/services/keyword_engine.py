"""
Keyword Normalization + Hashing Engine
=======================================
Core deduplication logic:
  1. Extract keywords from resume text
  2. Normalize (lowercase, dedup, remove stopwords, sort)
  3. Generate SHA-256 hash of the canonical keyword list

Two users with similar resumes → same hash → same Apify run → shared jobs.
"""

import hashlib
import json
import re

# ── Stopwords (common English words that don't help job matching) ─────────
STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "must",
    "i", "me", "my", "we", "our", "you", "your", "he", "she", "it",
    "they", "them", "their", "this", "that", "these", "those", "am",
    "not", "no", "nor", "so", "if", "as", "up", "out", "about", "into",
    "over", "after", "before", "between", "under", "above", "such",
    "each", "every", "all", "both", "few", "more", "most", "other",
    "some", "any", "only", "same", "than", "too", "very", "just",
    "also", "well", "how", "what", "when", "where", "which", "who",
    "whom", "why", "because", "while", "during", "through",
    # Resume noise
    "experience", "years", "year", "work", "working", "worked",
    "responsible", "responsibilities", "role", "currently", "present",
    "company", "team", "using", "used", "various", "including",
    "strong", "excellent", "good", "best", "great", "top",
    "ability", "skills", "knowledge",
    "proficient", "expertise", "understanding", "familiar", "etc",
})

# ── SAP-specific terms to always keep (even if short) ─────────────────────
SAP_TERMS = frozenset({
    "sap", "s/4hana", "s4hana", "ecc", "fico", "fi/co", "fi-co",
    "mm", "sd", "mdg", "lsmw", "ltmc", "slt", "cpi", "bapi", "idoc",
    "abap", "hana", "bw", "bw/4hana", "ewm", "tm", "pp", "pm", "ps",
    "hr", "hcm", "sf", "successfactors", "ariba", "concur",
    "p2p", "o2c", "procure-to-pay", "order-to-cash",
    "etl", "erp", "crm", "srm", "grc", "bpc", "apo",
    "fiori", "ui5", "odata", "rfc", "ale", "edi",
    "cutover", "go-live", "golive", "migration",
    "sit", "uat", "agile", "scrum", "jira", "smartsheet",
    "pmo", "program", "project", "manager", "consultant",
    "implementation", "rollout", "transformation",
    "data", "master", "governance",
})

# Minimum keyword length (except SAP terms)
MIN_KEYWORD_LEN = 3


def extract_keywords(resume_text: str) -> list[str]:
    """
    Extract meaningful keywords from resume text.

    Strategy:
      - Split on non-alphanumeric (keeping / and -)
      - Lowercase everything
      - Keep SAP terms regardless of length
      - Remove stopwords
      - Remove very short tokens
      - Also extract multi-word SAP phrases
    """
    text = resume_text.lower()

    # Extract multi-word SAP phrases first
    multi_word_patterns = [
        r"s/4\s*hana", r"sap\s+s/4\s*hana", r"sap\s+ecc",
        r"fi/co", r"fi-co",
        r"bw/4\s*hana",
        r"procure[- ]to[- ]pay", r"order[- ]to[- ]cash",
        r"data\s+migration", r"master\s+data",
        r"project\s+manager", r"program\s+manager",
        r"go[- ]live", r"solution\s+manager",
    ]

    found_phrases = set()
    for pattern in multi_word_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            # Normalize whitespace
            normalized = re.sub(r"\s+", " ", m).strip()
            found_phrases.add(normalized)

    # Split into single tokens
    tokens = re.split(r"[^a-z0-9/\-]+", text)

    keywords = set()
    for token in tokens:
        token = token.strip("-/")
        if not token:
            continue
        if token in STOPWORDS:
            continue
        if token in SAP_TERMS:
            keywords.add(token)
        elif len(token) >= MIN_KEYWORD_LEN:
            keywords.add(token)

    # Add multi-word phrases
    keywords.update(found_phrases)

    return sorted(keywords)


def normalize_keywords(keywords: list[str]) -> list[str]:
    """
    Normalize a keyword list for consistent hashing:
      1. Lowercase
      2. Strip whitespace
      3. Remove duplicates
      4. Remove stopwords
      5. Sort alphabetically
    """
    seen = set()
    result = []
    for kw in keywords:
        normalized = kw.lower().strip()
        if not normalized:
            continue
        if normalized in STOPWORDS:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    result.sort()
    return result


def hash_keywords(normalized_keywords: list[str]) -> str:
    """
    Generate a SHA-256 hash of the normalized keyword list.

    Same keywords in same order → same hash.
    Since normalize_keywords() sorts, order is deterministic.
    """
    canonical = json.dumps(normalized_keywords, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def process_resume_keywords(resume_text: str) -> tuple[list[str], str]:
    """
    Full pipeline: extract → normalize → hash.

    Returns (normalized_keywords, keyword_hash).
    """
    raw_keywords = extract_keywords(resume_text)
    normalized = normalize_keywords(raw_keywords)
    kw_hash = hash_keywords(normalized)
    return normalized, kw_hash
