"""
Tests for formatting / presentation methods:
  - get_cbc_report_with_ranges()
  - format_to_dataframe()
  - format_html_table()
  - extract_abnormal_values()
"""

import pytest
import pandas as pd
from lab_report_formatter import CBCReportFormatter


class TestGetCBCReportWithRanges:
    """Tests for get_cbc_report_with_ranges()."""

    def test_returns_dict(self, normal_report_text):
        result = CBCReportFormatter.get_cbc_report_with_ranges(normal_report_text)
        assert isinstance(result, dict)

    def test_each_entry_has_required_keys(self, normal_report_text):
        result = CBCReportFormatter.get_cbc_report_with_ranges(normal_report_text)
        for test_name, info in result.items():
            assert "Value" in info, f"{test_name} missing 'Value'"
            assert "Unit" in info, f"{test_name} missing 'Unit'"
            assert "Reference Range" in info, f"{test_name} missing 'Reference Range'"
            assert "Status" in info, f"{test_name} missing 'Status'"

    def test_status_is_normal_or_abnormal(self, normal_report_text):
        result = CBCReportFormatter.get_cbc_report_with_ranges(normal_report_text)
        for test_name, info in result.items():
            assert info["Status"] in ("Normal", "Abnormal"), (
                f"{test_name} has unexpected status: {info['Status']}"
            )

    def test_normal_values_have_normal_status(self, normal_report_text):
        """All values in the normal_report fixture are within range."""
        result = CBCReportFormatter.get_cbc_report_with_ranges(normal_report_text)
        if "Hemoglobin" in result:
            assert result["Hemoglobin"]["Status"] == "Normal"

    def test_abnormal_values_flagged(self, abnormal_report_text):
        """Hemoglobin 8.5 is below ref (10.0–17.0) → Abnormal."""
        result = CBCReportFormatter.get_cbc_report_with_ranges(abnormal_report_text)
        if "Hemoglobin" in result:
            assert result["Hemoglobin"]["Status"] == "Abnormal"

    def test_empty_text_returns_empty(self, empty_text):
        result = CBCReportFormatter.get_cbc_report_with_ranges(empty_text)
        assert len(result) == 0


class TestFormatToDataframe:
    """Tests for format_to_dataframe()."""

    def test_returns_dataframe(self, normal_report_text):
        values = CBCReportFormatter.parse_cbc_report(normal_report_text)
        df = CBCReportFormatter.format_to_dataframe(values)
        assert isinstance(df, pd.DataFrame)

    def test_expected_columns(self, normal_report_text):
        values = CBCReportFormatter.parse_cbc_report(normal_report_text)
        df = CBCReportFormatter.format_to_dataframe(values)
        expected_cols = {"Test Name", "Result", "Unit", "Reference Range", "Status"}
        assert set(df.columns) == expected_cols

    def test_row_count_matches_patterns(self, normal_report_text):
        """One row per pattern entry in PATTERNS dict (18 rows)."""
        values = CBCReportFormatter.parse_cbc_report(normal_report_text)
        df = CBCReportFormatter.format_to_dataframe(values)
        assert len(df) == len(CBCReportFormatter.PATTERNS)

    def test_missing_value_shows_dash(self, partial_report_text):
        """Parameters not found should show '—' as Result."""
        values = CBCReportFormatter.parse_cbc_report(partial_report_text)
        df = CBCReportFormatter.format_to_dataframe(values)
        mpv_row = df[df["Test Name"] == "MPV"]
        if not mpv_row.empty:
            assert mpv_row.iloc[0]["Result"] == "—"

    def test_empty_dict_all_dashes(self):
        """Empty values dict → every Result is '—'."""
        df = CBCReportFormatter.format_to_dataframe({})
        assert all(df["Result"] == "—")


class TestFormatHtmlTable:
    """Tests for format_html_table()."""

    def test_returns_string(self, normal_report_text):
        values = CBCReportFormatter.parse_cbc_report(normal_report_text)
        patient_info = CBCReportFormatter.extract_patient_info(normal_report_text)
        html = CBCReportFormatter.format_html_table(values, patient_info)
        assert isinstance(html, str)

    def test_contains_table_tag(self, normal_report_text):
        values = CBCReportFormatter.parse_cbc_report(normal_report_text)
        patient_info = CBCReportFormatter.extract_patient_info(normal_report_text)
        html = CBCReportFormatter.format_html_table(values, patient_info)
        assert "<table" in html
        assert "</table>" in html

    def test_contains_patient_name(self, normal_report_text):
        values = CBCReportFormatter.parse_cbc_report(normal_report_text)
        patient_info = CBCReportFormatter.extract_patient_info(normal_report_text)
        html = CBCReportFormatter.format_html_table(values, patient_info)
        # Patient name should appear in the HTML.
        assert patient_info["Name"] in html or "N/A" in html


class TestExtractAbnormalValues:
    """Tests for extract_abnormal_values()."""

    def test_no_abnormals_in_normal_report(self, normal_report_text):
        values = CBCReportFormatter.parse_cbc_report(normal_report_text)
        abnormals = CBCReportFormatter.extract_abnormal_values(values)
        assert len(abnormals) == 0, f"Unexpected abnormals: {abnormals}"

    def test_abnormal_hemoglobin_detected(self, abnormal_report_text):
        values = CBCReportFormatter.parse_cbc_report(abnormal_report_text)
        abnormals = CBCReportFormatter.extract_abnormal_values(values)
        if "Hemoglobin" in values:
            assert "Hemoglobin" in abnormals
            val, status = abnormals["Hemoglobin"]
            # 8.5 < 10.0 (min) → LOW
            assert status == "LOW"

    def test_abnormal_high_wbc(self, abnormal_report_text):
        values = CBCReportFormatter.parse_cbc_report(abnormal_report_text)
        abnormals = CBCReportFormatter.extract_abnormal_values(values)
        if "Total W.B.C. Count" in values:
            assert "Total W.B.C. Count" in abnormals
            val, status = abnormals["Total W.B.C. Count"]
            # 15000 > 10000 (max) → HIGH
            assert status == "HIGH"

    def test_empty_dict_no_abnormals(self):
        abnormals = CBCReportFormatter.extract_abnormal_values({})
        assert len(abnormals) == 0

    def test_return_type_is_dict(self, normal_report_text):
        values = CBCReportFormatter.parse_cbc_report(normal_report_text)
        abnormals = CBCReportFormatter.extract_abnormal_values(values)
        assert isinstance(abnormals, dict)
