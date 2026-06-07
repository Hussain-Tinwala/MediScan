"""
Tests for the module-level format_report_for_display() function.

This function orchestrates the full pipeline:
  parse patient info → parse CBC → format HTML → build summary string

Returns: Tuple[Dict, str, str]  →  (cbc_values, html_table, summary)
"""

import pytest
from lab_report_formatter import format_report_for_display


class TestFormatReportForDisplay:
    """Tests for the public pipeline entry point."""

    def test_returns_three_element_tuple(self, normal_report_text):
        result = format_report_for_display(normal_report_text)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_first_element_is_dict(self, normal_report_text):
        cbc_values, _, _ = format_report_for_display(normal_report_text)
        assert isinstance(cbc_values, dict)

    def test_second_element_is_html_string(self, normal_report_text):
        _, html, _ = format_report_for_display(normal_report_text)
        assert isinstance(html, str)
        assert "<table" in html

    def test_third_element_is_summary_string(self, normal_report_text):
        _, _, summary = format_report_for_display(normal_report_text)
        assert isinstance(summary, str)

    def test_disease_type_appears_in_summary(self, normal_report_text):
        _, _, summary = format_report_for_display(normal_report_text, "dengue")
        assert "DENGUE" in summary

    def test_default_disease_type_is_general(self, normal_report_text):
        _, _, summary = format_report_for_display(normal_report_text)
        assert "GENERAL" in summary

    def test_normal_report_summary_all_normal(self, normal_report_text):
        """When all values are within range, summary says so."""
        _, _, summary = format_report_for_display(normal_report_text)
        assert "normal range" in summary.lower() or "Normal" in summary

    def test_abnormal_report_summary_flags_issues(self, abnormal_report_text):
        """When abnormal values exist, they appear in the summary."""
        _, _, summary = format_report_for_display(abnormal_report_text)
        assert "Abnormal" in summary or "⚠️" in summary

    def test_empty_text(self, empty_text):
        cbc_values, html, summary = format_report_for_display(empty_text)
        assert isinstance(cbc_values, dict)
        assert len(cbc_values) == 0

    def test_patient_name_in_summary(self, normal_report_text):
        _, _, summary = format_report_for_display(normal_report_text)
        # Either actual name or N/A should appear.
        assert "Rahul Sharma" in summary or "N/A" in summary
