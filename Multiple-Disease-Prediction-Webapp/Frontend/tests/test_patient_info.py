"""
Tests for CBCReportFormatter.extract_patient_info()

Extracts patient demographics (Name, Gender, Age, Sample ID, Date, Lab,
Branch, Contact) from free-form OCR text.  Tests cover:
  - Full demographics with all fields present
  - Minimal text with no demographics → all fields default to "N/A"
  - Partial demographics — some fields present, others N/A
  - Different delimiters (colon, dash, space)
  - Mixed-case field labels
"""

import pytest
from lab_report_formatter import CBCReportFormatter


class TestExtractPatientInfo:
    """Tests for the extract_patient_info static method."""

    # ======================== FULL DEMOGRAPHICS ========================

    def test_full_patient_info(self, patient_info_full_text):
        """All demographic fields are extracted from a well-formatted report."""
        info = CBCReportFormatter.extract_patient_info(patient_info_full_text)

        # Name must be cleaned (extra spaces collapsed) and non-empty.
        assert info["Name"] == "Ananya Deshmukh"
        # The regex ([MFmf]|Male|Female) matches single letter 'F' before 'Female'.
        assert info["Gender"] in ("F", "Female")
        # Age is a string of digits.
        assert info["Age"] == "42"
        # Sample ID extracted from "Sample ID: 789012".
        assert info["Sample ID"] == "789012"
        # Date extracted from "Report Date: 20-04-2025 14:00".
        assert "20-04-2025" in info["Date"]
        # Lab name detected from all-caps line containing "PATHOLOGY".
        assert "PATHOLOGY" in info["Lab"].upper()
        # Branch extracted.
        assert info["Branch"] == "Bandra"
        # Contact number extracted.
        assert "9988776655" in info["Contact"]

    # ======================== MISSING DEMOGRAPHICS ========================

    def test_minimal_text_defaults_to_na(self, patient_info_minimal_text):
        """When no demographics are present, every field defaults to 'N/A'."""
        info = CBCReportFormatter.extract_patient_info(patient_info_minimal_text)

        # Name should be N/A since there is no "Name:" or "Patient:" line.
        assert info["Name"] == "N/A"
        assert info["Gender"] == "N/A"
        assert info["Age"] == "N/A"
        assert info["Sample ID"] == "N/A"
        assert info["Date"] == "N/A"

    def test_empty_string(self):
        """Empty input produces all N/A values."""
        info = CBCReportFormatter.extract_patient_info("")
        assert info["Name"] == "N/A"
        assert info["Gender"] == "N/A"
        assert info["Age"] == "N/A"

    # ======================== PARTIAL DEMOGRAPHICS ========================

    def test_name_and_age_only(self):
        """When only name and age are present, other fields are N/A."""
        text = "Name: John Doe\nAge: 55\nHemoglobin: 14.0"
        info = CBCReportFormatter.extract_patient_info(text)
        assert info["Name"] == "John Doe"
        assert info["Age"] == "55"
        assert info["Gender"] == "N/A"
        assert info["Sample ID"] == "N/A"

    # ======================== FORMAT VARIATIONS ========================

    def test_gender_single_letter(self):
        """Gender given as single letter 'M' or 'F' is accepted."""
        text = "Name: Test Patient\nGender: M\nAge: 30"
        info = CBCReportFormatter.extract_patient_info(text)
        assert info["Gender"] == "M"

    def test_gender_lowercase(self):
        """Lowercase gender label is handled via case-insensitive regex."""
        text = "Name: Test Patient\ngender: female\nAge: 25"
        info = CBCReportFormatter.extract_patient_info(text)
        # The alternation [MFmf] matches first, so we get 'f' not 'female'.
        assert info["Gender"].lower() in ("f", "female")

    def test_sex_label_instead_of_gender(self):
        """'Sex' is an alternative label for gender."""
        text = "Name: Amit Kumar\nSex: Male\nAge: 40"
        info = CBCReportFormatter.extract_patient_info(text)
        # Regex alternation may match 'M' before 'Male'.
        assert info["Gender"] in ("M", "Male")

    def test_specimen_id_alias(self):
        """'Specimen ID' is recognised as an alias for Sample ID."""
        text = "Name: Test\nSpecimen ID: 999888\nAge: 20"
        info = CBCReportFormatter.extract_patient_info(text)
        assert info["Sample ID"] == "999888"

    # ======================== RETURN TYPE GUARANTEES ========================

    def test_return_type_is_dict(self):
        """The return value is always a dict."""
        info = CBCReportFormatter.extract_patient_info("any text")
        assert isinstance(info, dict)

    def test_required_keys_always_present(self):
        """Name, Gender, Age, Sample ID, Date, Lab, Branch, Contact are always in the dict."""
        info = CBCReportFormatter.extract_patient_info("")
        for key in ["Name", "Gender", "Age", "Sample ID", "Date", "Lab", "Branch", "Contact"]:
            assert key in info, f"Missing key: {key}"
