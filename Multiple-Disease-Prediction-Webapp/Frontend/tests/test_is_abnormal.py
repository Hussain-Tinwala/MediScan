"""
Tests for CBCReportFormatter.is_abnormal()

This method checks whether a given float value falls outside an inclusive
[min_val, max_val] reference range.  Tests cover:
  - Values within range (returns False)
  - Values below range (returns True)
  - Values above range (returns True)
  - Values exactly at boundary (returns False — boundaries are normal)
  - None value (returns False — missing data is not flagged abnormal)
"""

import pytest
from lab_report_formatter import CBCReportFormatter


class TestIsAbnormal:
    """Tests for the is_abnormal static method."""

    # ======================== WITHIN RANGE ========================

    def test_value_within_range(self):
        """A value squarely inside the range is Normal."""
        # Hemoglobin ref range: 10.0–17.0; 14.0 is well inside.
        assert CBCReportFormatter.is_abnormal(14.0, 10.0, 17.0) is False

    def test_value_at_midpoint(self):
        """Midpoint of the range is Normal."""
        assert CBCReportFormatter.is_abnormal(13.5, 10.0, 17.0) is False

    # ======================== AT BOUNDARIES ========================

    def test_value_at_lower_boundary(self):
        """A value exactly at the minimum is considered Normal (inclusive)."""
        # 10.0 == min_val → not abnormal.
        assert CBCReportFormatter.is_abnormal(10.0, 10.0, 17.0) is False

    def test_value_at_upper_boundary(self):
        """A value exactly at the maximum is considered Normal (inclusive)."""
        # 17.0 == max_val → not abnormal.
        assert CBCReportFormatter.is_abnormal(17.0, 10.0, 17.0) is False

    # ======================== OUTSIDE RANGE ========================

    def test_value_below_range(self):
        """A value just below the minimum is Abnormal."""
        assert CBCReportFormatter.is_abnormal(9.9, 10.0, 17.0) is True

    def test_value_above_range(self):
        """A value just above the maximum is Abnormal."""
        assert CBCReportFormatter.is_abnormal(17.1, 10.0, 17.0) is True

    def test_severely_low(self):
        """Extremely low value is Abnormal."""
        assert CBCReportFormatter.is_abnormal(3.0, 10.0, 17.0) is True

    def test_severely_high(self):
        """Extremely high value is Abnormal."""
        assert CBCReportFormatter.is_abnormal(25.0, 10.0, 17.0) is True

    # ======================== SPECIAL CASES ========================

    def test_none_value(self):
        """None signals missing data and should NOT be flagged abnormal."""
        # The implementation guards against None with an early return.
        assert CBCReportFormatter.is_abnormal(None, 10.0, 17.0) is False

    def test_zero_range(self):
        """When min == max, only that exact value is normal."""
        assert CBCReportFormatter.is_abnormal(0.0, 0.0, 0.0) is False
        assert CBCReportFormatter.is_abnormal(0.1, 0.0, 0.0) is True

    def test_zero_value_within_range(self):
        """Zero is valid when the range includes zero (e.g. Basophils 0–1)."""
        assert CBCReportFormatter.is_abnormal(0.0, 0.0, 1.0) is False
