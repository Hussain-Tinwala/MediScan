"""
Tests for CBCReportFormatter._validate_value()

Rules:
  - Percentage-based tests: 0–100.
  - Absolute counts / cell counts: >= 0.
  - Other tests: within 50% margin of reference range.
  - Unknown test names: always valid.
"""

import pytest
from lab_report_formatter import CBCReportFormatter


class TestValidateValue:

    def test_neutrophils_valid_percentage(self):
        assert CBCReportFormatter._validate_value("Neutrophils", 60.0) is True

    def test_neutrophils_zero(self):
        assert CBCReportFormatter._validate_value("Neutrophils", 0.0) is True

    def test_neutrophils_100(self):
        assert CBCReportFormatter._validate_value("Neutrophils", 100.0) is True

    def test_neutrophils_over_100(self):
        assert CBCReportFormatter._validate_value("Neutrophils", 101.0) is False

    def test_neutrophils_negative(self):
        assert CBCReportFormatter._validate_value("Neutrophils", -1.0) is False

    def test_lymphocytes_valid(self):
        assert CBCReportFormatter._validate_value("Lymphocytes", 35.0) is True

    def test_basophils_valid(self):
        assert CBCReportFormatter._validate_value("Basophils", 0.5) is True

    def test_haematocrit_valid(self):
        assert CBCReportFormatter._validate_value("Haematocrit (PCV/HCT)", 44.0) is True

    def test_neutrophils_abs_valid(self):
        assert CBCReportFormatter._validate_value("Neutrophils (abs)", 4500.0) is True

    def test_neutrophils_abs_zero(self):
        assert CBCReportFormatter._validate_value("Neutrophils (abs)", 0.0) is True

    def test_platelet_count_valid(self):
        assert CBCReportFormatter._validate_value("Platelet Count", 250000.0) is True

    def test_platelet_count_zero(self):
        assert CBCReportFormatter._validate_value("Platelet Count", 0.0) is True

    def test_wbc_count_valid(self):
        assert CBCReportFormatter._validate_value("Total W.B.C. Count", 7500.0) is True

    def test_hemoglobin_within_range(self):
        assert CBCReportFormatter._validate_value("Hemoglobin", 14.5) is True

    def test_hemoglobin_within_margin(self):
        """8.0 is below ref range but within 50% margin."""
        assert CBCReportFormatter._validate_value("Hemoglobin", 8.0) is True

    def test_hemoglobin_outside_margin(self):
        """2.0 is far below the 50%-margin lower bound."""
        assert CBCReportFormatter._validate_value("Hemoglobin", 2.0) is False

    def test_mcv_valid(self):
        assert CBCReportFormatter._validate_value("Mean Corpuscular Volume (M.C.V.)", 88.0) is True

    def test_mch_valid(self):
        assert CBCReportFormatter._validate_value("Mean Corpuscular Hb (M.C.H.)", 29.5) is True

    def test_rbc_valid(self):
        assert CBCReportFormatter._validate_value("Total R.B.C. Count", 5.1) is True

    def test_unknown_test_always_valid(self):
        assert CBCReportFormatter._validate_value("Unknown Test XYZ", 99999.0) is True
