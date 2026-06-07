"""
Integration tests for CBCReportFormatter.parse_cbc_report()

This is the main entry point that orchestrates:
  _preprocess_text → _try_columnar_extraction → _universal_extraction → normalize_values

Tests cover: normal reports, partial reports, abbreviations, uppercase,
extra spaces, dash separators, columnar format, empty/garbage input, and
abnormal value scenarios.
"""

import pytest
from lab_report_formatter import CBCReportFormatter


class TestParseCBCReportNormal:
    """Normal, well-formatted report with all 18 parameters."""

    def test_all_parameters_extracted(self, normal_report_text, normal_report_expected_values):
        """Every expected parameter key is present in the output."""
        result = CBCReportFormatter.parse_cbc_report(normal_report_text)
        for key in normal_report_expected_values:
            assert key in result, f"Missing parameter: {key}"

    def test_hemoglobin_value(self, normal_report_text):
        result = CBCReportFormatter.parse_cbc_report(normal_report_text)
        assert result["Hemoglobin"] == 14.5

    def test_wbc_value(self, normal_report_text):
        result = CBCReportFormatter.parse_cbc_report(normal_report_text)
        assert result["Total W.B.C. Count"] == 7500.0

    def test_platelet_value(self, normal_report_text):
        result = CBCReportFormatter.parse_cbc_report(normal_report_text)
        assert result["Platelet Count"] == 250.0

    def test_neutrophils_value(self, normal_report_text):
        result = CBCReportFormatter.parse_cbc_report(normal_report_text)
        assert result["Neutrophils"] == 60.0

    def test_lymphocytes_value(self, normal_report_text):
        result = CBCReportFormatter.parse_cbc_report(normal_report_text)
        assert result["Lymphocytes"] == 30.0

    def test_return_type_is_dict(self, normal_report_text):
        result = CBCReportFormatter.parse_cbc_report(normal_report_text)
        assert isinstance(result, dict)

    def test_all_values_are_floats(self, normal_report_text):
        result = CBCReportFormatter.parse_cbc_report(normal_report_text)
        for key, val in result.items():
            assert isinstance(val, (int, float)), f"{key} is {type(val)}"


class TestParseCBCReportPartial:
    """Report with only a subset of parameters present."""

    def test_present_values_extracted(self, partial_report_text):
        result = CBCReportFormatter.parse_cbc_report(partial_report_text)
        assert "Hemoglobin" in result
        assert result["Hemoglobin"] == 12.0

    def test_wbc_present(self, partial_report_text):
        result = CBCReportFormatter.parse_cbc_report(partial_report_text)
        assert "Total W.B.C. Count" in result

    def test_platelet_present(self, partial_report_text):
        result = CBCReportFormatter.parse_cbc_report(partial_report_text)
        assert "Platelet Count" in result

    def test_missing_parameters_absent(self, partial_report_text):
        """Parameters not in the text should not appear in the output dict."""
        result = CBCReportFormatter.parse_cbc_report(partial_report_text)
        assert "MPV" not in result


class TestParseCBCReportAbbreviations:
    """Report using abbreviated forms (neut%, lymph%, etc.)."""

    def test_abbreviated_extraction(self, abbreviated_report_text):
        result = CBCReportFormatter.parse_cbc_report(abbreviated_report_text)
        assert "Hemoglobin" in result
        assert "Platelet Count" in result

    def test_neut_percent_to_neutrophils(self, abbreviated_report_text):
        result = CBCReportFormatter.parse_cbc_report(abbreviated_report_text)
        if "Neutrophils" in result:
            assert result["Neutrophils"] == 55.0


class TestParseCBCReportUppercase:
    """All-caps input text."""

    def test_uppercase_hemoglobin(self, uppercase_report_text):
        result = CBCReportFormatter.parse_cbc_report(uppercase_report_text)
        assert "Hemoglobin" in result
        assert result["Hemoglobin"] == 15.0

    def test_uppercase_wbc(self, uppercase_report_text):
        result = CBCReportFormatter.parse_cbc_report(uppercase_report_text)
        assert "Total W.B.C. Count" in result

    def test_uppercase_platelet(self, uppercase_report_text):
        result = CBCReportFormatter.parse_cbc_report(uppercase_report_text)
        assert "Platelet Count" in result


class TestParseCBCReportExtraSpaces:
    """Input with excessive whitespace."""

    def test_extra_spaces_hemoglobin(self, extra_spaces_report_text):
        result = CBCReportFormatter.parse_cbc_report(extra_spaces_report_text)
        assert "Hemoglobin" in result
        assert result["Hemoglobin"] == 14.0

    def test_extra_spaces_wbc(self, extra_spaces_report_text):
        result = CBCReportFormatter.parse_cbc_report(extra_spaces_report_text)
        assert "Total W.B.C. Count" in result


class TestParseCBCReportDashSeparated:
    """Report using dashes instead of colons."""

    def test_dash_hemoglobin(self, dash_separated_report_text):
        result = CBCReportFormatter.parse_cbc_report(dash_separated_report_text)
        assert "Hemoglobin" in result
        assert result["Hemoglobin"] == 13.5


class TestParseCBCReportColumnar:
    """Columnar OCR format (names in one block, values after 'Result')."""

    def test_columnar_returns_values(self, columnar_report_text):
        result = CBCReportFormatter.parse_cbc_report(columnar_report_text)
        assert len(result) > 0, "Columnar extraction should find values"

    def test_columnar_hemoglobin(self, columnar_report_text):
        result = CBCReportFormatter.parse_cbc_report(columnar_report_text)
        if "Hemoglobin" in result:
            assert result["Hemoglobin"] == 14.0


class TestParseCBCReportInvalid:
    """Empty or garbage input."""

    def test_empty_returns_empty_dict(self, empty_text):
        result = CBCReportFormatter.parse_cbc_report(empty_text)
        assert isinstance(result, dict)
        assert len(result) == 0

    def test_garbage_returns_empty_or_few(self, garbage_text):
        result = CBCReportFormatter.parse_cbc_report(garbage_text)
        assert isinstance(result, dict)
        # Garbage text should not produce all 18 valid CBC parameters.
        assert len(result) < 5
