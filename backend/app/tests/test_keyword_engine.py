"""
Tests for the keyword normalization + hashing engine.

These tests verify the core deduplication logic without needing
any external services (no DB, no Redis, no Apify).
"""

from backend.app.services.keyword_engine import (
    extract_keywords,
    normalize_keywords,
    hash_keywords,
    process_resume_keywords,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Test: Keyword Extraction
# ═══════════════════════════════════════════════════════════════════════════════

class TestExtractKeywords:
    def test_extracts_sap_terms(self):
        text = "Experienced SAP S/4HANA consultant with FICO and MM expertise"
        keywords = extract_keywords(text)
        assert "sap" in keywords
        assert "s/4hana" in keywords or "s/4 hana" in keywords or "sap s/4 hana" in keywords
        assert "fico" in keywords
        assert "mm" in keywords
        assert "consultant" in keywords

    def test_extracts_multi_word_phrases(self):
        text = "Led data migration projects and program manager responsibilities"
        keywords = extract_keywords(text)
        assert "data migration" in keywords
        assert "program manager" in keywords

    def test_removes_stopwords(self):
        text = "I am a very experienced SAP consultant with excellent skills"
        keywords = extract_keywords(text)
        assert "i" not in keywords
        assert "am" not in keywords
        assert "very" not in keywords
        assert "with" not in keywords
        assert "sap" in keywords
        assert "consultant" in keywords

    def test_empty_text(self):
        assert extract_keywords("") == []

    def test_returns_sorted(self):
        text = "python fastapi aws sap"
        keywords = extract_keywords(text)
        assert keywords == sorted(keywords)


# ═══════════════════════════════════════════════════════════════════════════════
# Test: Keyword Normalization
# ═══════════════════════════════════════════════════════════════════════════════

class TestNormalizeKeywords:
    def test_lowercases(self):
        result = normalize_keywords(["SAP", "FICO", "Python"])
        assert all(kw == kw.lower() for kw in result)

    def test_removes_duplicates(self):
        result = normalize_keywords(["sap", "fico", "sap", "fico"])
        assert result == ["fico", "sap"]

    def test_removes_stopwords(self):
        result = normalize_keywords(["sap", "the", "and", "fico"])
        assert "the" not in result
        assert "and" not in result
        assert "sap" in result

    def test_sorts_alphabetically(self):
        result = normalize_keywords(["python", "aws", "fastapi"])
        assert result == ["aws", "fastapi", "python"]

    def test_strips_whitespace(self):
        result = normalize_keywords(["  sap  ", " fico "])
        assert result == ["fico", "sap"]

    def test_empty_list(self):
        assert normalize_keywords([]) == []


# ═══════════════════════════════════════════════════════════════════════════════
# Test: Keyword Hashing
# ═══════════════════════════════════════════════════════════════════════════════

class TestHashKeywords:
    def test_deterministic(self):
        kw = ["aws", "fastapi", "python"]
        h1 = hash_keywords(kw)
        h2 = hash_keywords(kw)
        assert h1 == h2

    def test_sha256_format(self):
        h = hash_keywords(["sap", "fico"])
        assert len(h) == 64  # SHA-256 hex digest
        assert all(c in "0123456789abcdef" for c in h)

    def test_different_keywords_different_hash(self):
        h1 = hash_keywords(["sap", "fico"])
        h2 = hash_keywords(["sap", "mm"])
        assert h1 != h2

    def test_order_matters(self):
        """Since normalize_keywords sorts, this tests that raw order affects hash."""
        h1 = hash_keywords(["a", "b"])
        h2 = hash_keywords(["b", "a"])
        # Different order = different hash (normalization handles sorting)
        assert h1 != h2


# ═══════════════════════════════════════════════════════════════════════════════
# Test: Full Pipeline (extract → normalize → hash)
# ═══════════════════════════════════════════════════════════════════════════════

class TestProcessResumeKeywords:
    def test_full_pipeline(self):
        text = "SAP S/4HANA Program Manager with FICO and MM experience"
        keywords, kw_hash = process_resume_keywords(text)
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert isinstance(kw_hash, str)
        assert len(kw_hash) == 64

    def test_same_resume_same_hash(self):
        """Core dedup test: same resume → same hash."""
        text = "SAP FICO consultant with data migration and S/4HANA experience"
        _, h1 = process_resume_keywords(text)
        _, h2 = process_resume_keywords(text)
        assert h1 == h2

    def test_similar_resumes_same_hash(self):
        """Resumes with same keywords in different order → same hash."""
        text1 = "SAP FICO consultant with data migration"
        text2 = "data migration consultant SAP FICO"
        kw1, h1 = process_resume_keywords(text1)
        kw2, h2 = process_resume_keywords(text2)
        # Both should extract the same normalized keywords
        assert kw1 == kw2
        assert h1 == h2

    def test_different_resumes_different_hash(self):
        """Genuinely different resumes → different hash."""
        text1 = "SAP FICO consultant with general ledger expertise"
        text2 = "Python developer with AWS and React experience"
        _, h1 = process_resume_keywords(text1)
        _, h2 = process_resume_keywords(text2)
        assert h1 != h2

    def test_keywords_are_sorted(self):
        text = "python fastapi aws sap fico"
        keywords, _ = process_resume_keywords(text)
        assert keywords == sorted(keywords)

    def test_no_stopwords_in_output(self):
        text = "I am the best SAP consultant with excellent experience in FICO"
        keywords, _ = process_resume_keywords(text)
        for sw in ["i", "am", "the", "best", "with", "in"]:
            assert sw not in keywords
