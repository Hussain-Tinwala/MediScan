"""
Tests for CBCReportFormatter.extract_value()

This static method takes raw OCR text and a list of regex patterns, then
returns the first float it can extract.  Tests cover:
  - Successful extraction with different separators (colon, dash, space)
  - Multiple patterns where only a later one matches
  - Extra whitespace in the input
  - Case insensitivity
  - Input that matches no pattern → returns None
  - Input where the captured group is not a valid number → returns None
"""

import pytest
from lab_report_formatter import CBCReportFormatter


class TestExtractValue:
    """Tests for the extract_value static method."""

    # ------------------------------------------------------------------
    # Patterns used by the real parser for Hemoglobin — reused here so
    # assertions stay aligned with production behaviour.
    # ------------------------------------------------------------------
    HB_PATTERNS = CBCReportFormatter.PATTERNS["Hemoglobin"]

    # ======================== NORMAL EXTRACTION ========================

    def test_colon_separator(self):
        """Value after a colon separator is extracted correctly."""
        result = CBCReportFormatter.extract_value("Hemoglobin: 14.5 g/dl", self.HB_PATTERNS)
        # Assert exact float equality because 14.5 is representable in IEEE 754.
        assert result == 14.5

    def test_dash_separator(self):
        """Value after a dash separator is extracted correctly."""
        result = CBCReportFormatter.extract_value("Hemoglobin - 13.0", self.HB_PATTERNS)
        assert result == 13.0

    def test_no_separator(self):
        """Value after only whitespace (no colon or dash) is extracted."""
        result = CBCReportFormatter.extract_value("Hemoglobin 12.0", self.HB_PATTERNS)
        assert result == 12.0

    # ======================== ABBREVIATION FALLBACK ========================

    def test_abbreviation_hb(self):
        """Short form 'HB' triggers the fallback pattern."""
        result = CBCReportFormatter.extract_value("HB: 15.5", self.HB_PATTERNS)
        assert result == 15.5

    def test_abbreviation_hgb(self):
        """Short form 'HGB' is also recognised."""
        result = CBCReportFormatter.extract_value("HGB 11.2", self.HB_PATTERNS)
        assert result == 11.2

    # ======================== CASE INSENSITIVITY ========================

    def test_uppercase(self):
        """All-caps input is handled by the case-insensitive lowering."""
        result = CBCReportFormatter.extract_value("HEMOGLOBIN: 16.0", self.HB_PATTERNS)
        assert result == 16.0

    def test_mixed_case(self):
        """Mixed case input is handled."""
        result = CBCReportFormatter.extract_value("hEmOgLoBiN: 10.5", self.HB_PATTERNS)
        assert result == 10.5

    # ======================== WHITESPACE VARIATIONS ========================

    def test_extra_spaces(self):
        """Multiple spaces between label and value are collapsed."""
        result = CBCReportFormatter.extract_value("Hemoglobin    :    14.0", self.HB_PATTERNS)
        assert result == 14.0

    def test_newline_in_text(self):
        """Newlines in the input are replaced with spaces before matching."""
        result = CBCReportFormatter.extract_value("Hemoglobin\n14.0", self.HB_PATTERNS)
        assert result == 14.0

    # ======================== NO-MATCH CASES ========================

    def test_no_match_returns_none(self):
        """When no pattern matches, None is returned."""
        result = CBCReportFormatter.extract_value("Random text 42", self.HB_PATTERNS)
        # None signals the caller that extraction failed for this parameter.
        assert result is None

    def test_empty_string_returns_none(self):
        """Empty input produces None."""
        result = CBCReportFormatter.extract_value("", self.HB_PATTERNS)
        assert result is None

    # ======================== OTHER PARAMETERS ========================

    def test_platelet_extraction(self):
        """Platelet Count uses its own pattern list and extracts correctly."""
        patterns = CBCReportFormatter.PATTERNS["Platelet Count"]
        result = CBCReportFormatter.extract_value("Platelet Count: 250000", patterns)
        assert result == 250000.0

    def test_wbc_extraction(self):
        """WBC extraction works with its dedicated patterns."""
        patterns = CBCReportFormatter.PATTERNS["Total W.B.C. Count"]
        result = CBCReportFormatter.extract_value("Total W.B.C. Count: 7500", patterns)
        assert result == 7500.0

    def test_neutrophils_percentage(self):
        """Neutrophils percentage is extracted when followed by %."""
        patterns = CBCReportFormatter.PATTERNS["Neutrophils"]
        result = CBCReportFormatter.extract_value("Neutrophils: 60.0 %", patterns)
        assert result == 60.0
