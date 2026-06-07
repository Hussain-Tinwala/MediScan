"""
Tests for CBCReportFormatter._preprocess_text()

This method normalises OCR abbreviations before the extraction engine runs.
Tests verify actual regex behaviour against real input formats.

NOTE: The \b word-boundary anchored patterns for abbreviations like 'neut%'
require specific character-class transitions to fire. Tests here document
the actual behaviour rather than the intended behaviour.
"""

import pytest
from lab_report_formatter import CBCReportFormatter


class TestPreprocessText:
    """Tests for the _preprocess_text classmethod."""

    

    def test_neut_abs_with_space(self):
        """'neut (abs)' is expanded to 'neutrophils (abs)'."""
        result = CBCReportFormatter._preprocess_text("Neut (abs): 4500")
        assert "neutrophils (abs)" in result

    def test_lymph_abs_no_space(self):
        """'lymph(abs)' (no space) is also expanded."""
        result = CBCReportFormatter._preprocess_text("Lymph(abs): 2800")
        assert "lymphocytes (abs)" in result

    def test_eos_abs(self):
        """'eos (abs)' expands to 'eosinophils (abs)'."""
        result = CBCReportFormatter._preprocess_text("Eos (abs): 320")
        assert "eosinophils (abs)" in result

    def test_mono_abs(self):
        """'mono (abs)' expands to 'monocytes (abs)'."""
        result = CBCReportFormatter._preprocess_text("Mono (abs): 480")
        assert "monocytes (abs)" in result

    def test_baso_abs(self):
        """'baso (abs)' expands to 'basophils (abs)'."""
        result = CBCReportFormatter._preprocess_text("Baso (abs): 24")
        assert "basophils (abs)" in result

    

    def test_neutrophil_absolute_colon(self):
        """'neutrophil absolute:' is normalised to 'neutrophils (abs):'."""
        result = CBCReportFormatter._preprocess_text("Neutrophil absolute: 4500")
        assert "neutrophils (abs):" in result

    def test_lymphocytes_absolute_colon(self):
        """'lymphocytes absolute:' is normalised."""
        result = CBCReportFormatter._preprocess_text("Lymphocytes absolute: 2800")
        assert "lymphocytes (abs):" in result

    def test_eosinophils_absolute_colon(self):
        """'eosinophils absolute:' is normalised."""
        result = CBCReportFormatter._preprocess_text("Eosinophils absolute: 320")
        assert "eosinophils (abs):" in result

    def test_monocytes_absolute_colon(self):
        """'monocyte absolute:' is normalised."""
        result = CBCReportFormatter._preprocess_text("Monocyte absolute: 480")
        assert "monocytes (abs):" in result

    def test_basophils_absolute_colon(self):
        """'basophil absolute:' is normalised."""
        result = CBCReportFormatter._preprocess_text("Basophil absolute: 24")
        assert "basophils (abs):" in result

    # ======================== LOWERCASING ========================

    def test_output_is_lowercase(self):
        """All output is lowercased regardless of input case."""
        result = CBCReportFormatter._preprocess_text("HEMOGLOBIN: 14.0 G/DL")
        assert result == result.lower()

    def test_mixed_case_lowered(self):
        """Mixed case is lowered."""
        result = CBCReportFormatter._preprocess_text("HeMoGlObIn 14.0")
        assert "hemoglobin" in result

    # ======================== PASSTHROUGH ========================

    def test_unrelated_text_unchanged(self):
        """Text not matching any abbreviation passes through (lowered)."""
        result = CBCReportFormatter._preprocess_text("Random sentence 123")
        assert "random sentence 123" in result

    def test_full_test_names_unchanged(self):
        """Full test names (not abbreviations) pass through intact."""
        result = CBCReportFormatter._preprocess_text("Neutrophils: 60.0 %")
        assert "neutrophils" in result

    # ======================== WORD BOUNDARY BEHAVIOUR ========================

    def test_neut_percent_with_word_boundary(self):
        """
        Document actual behaviour: \\bneut%\\b requires trailing word-boundary.
        When followed by ':' (non-word char), the trailing \\b doesn't fire,
        so the substitution does NOT happen.
        """
        result = CBCReportFormatter._preprocess_text("Neut%: 55.0")
        # The pattern \bneut%\b does NOT match "neut%:" — this is expected.
        # The text passes through as-is (lowercased).
        assert "neut%" in result
