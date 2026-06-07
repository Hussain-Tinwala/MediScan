"""
Shared pytest fixtures for CBC Report Parser tests.

All synthetic report texts are defined here so individual test modules
can reuse them without duplication.  Every fixture is session-scoped
(created once per test run) because the text data is read-only.
"""

import sys
import os
import pytest

# ---------------------------------------------------------------------------
# Add the Frontend directory to sys.path so that `lab_report_formatter`
# can be imported directly (mirrors how the Streamlit app uses it).
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lab_report_formatter import CBCReportFormatter, format_report_for_display


# ===================== FORMATTER INSTANCE =====================


@pytest.fixture(scope="session")
def formatter():
    """Return a CBCReportFormatter instance (stateless, safe to share)."""
    return CBCReportFormatter()


# ===================== SYNTHETIC OCR TEXTS =====================


@pytest.fixture(scope="session")
def normal_report_text():
    """A well-formatted CBC report with ALL 18 parameters present."""
    return (
        "MEDILAB DIAGNOSTIC CENTRE\n"
        "Branch: Andheri\n"
        "Contact: +91-9876543210\n"
        "\n"
        "Name: Rahul Sharma  Gender: Male  Age: 35\n"
        "Sample ID: 123456\n"
        "Report Date: 15-03-2025 10:30\n"
        "\n"
        "COMPLETE BLOOD COUNT (CBC)\n"
        "\n"
        "Hemoglobin: 14.5 g/dl\n"
        "Total R.B.C. Count: 5.1 millions/cumm\n"
        "Haematocrit (PCV/HCT): 44.0 %\n"
        "Mean Corpuscular Volume (M.C.V.): 88.0 fl\n"
        "Mean Corpuscular Hb (M.C.H.): 29.5 Pg\n"
        "Total W.B.C. Count: 7500 /uL\n"
        "Neutrophils: 60.0 %\n"
        "Lymphocytes: 30.0 %\n"
        "Eosinophils: 3.0 %\n"
        "Monocytes: 5.0 %\n"
        "Basophils: 0.5 %\n"
        "Platelet Count: 250 /uL\n"
        "MPV: 10.2 fL\n"
        "Neutrophils (abs): 4500 /uL\n"
        "Lymphocytes (abs): 2250 /uL\n"
        "Eosinophils (abs): 225 /uL\n"
        "Monocytes (abs): 375 /uL\n"
        "Basophils (abs): 37 /uL\n"
    )


@pytest.fixture(scope="session")
def normal_report_expected_values():
    """Expected extraction results for the normal report."""
    return {
        "Hemoglobin": 14.5,
        "Total R.B.C. Count": 5.1,
        "Haematocrit (PCV/HCT)": 44.0,
        "Mean Corpuscular Volume (M.C.V.)": 88.0,
        "Mean Corpuscular Hb (M.C.H.)": 29.5,
        "Total W.B.C. Count": 7500.0,
        "Neutrophils": 60.0,
        "Lymphocytes": 30.0,
        "Eosinophils": 3.0,
        "Monocytes": 5.0,
        "Basophils": 0.5,
        "Platelet Count": 250.0,
        "MPV": 10.2,
        "Neutrophils (abs)": 4500.0,
        "Lymphocytes (abs)": 2250.0,
        "Eosinophils (abs)": 225.0,
        "Monocytes (abs)": 375.0,
        "Basophils (abs)": 37.0,
    }


@pytest.fixture(scope="session")
def partial_report_text():
    """Report with only a few parameters — the rest should be absent."""
    return (
        "Name: Priya Patel  Gender: Female  Age: 28\n"
        "\n"
        "Hemoglobin: 12.0 g/dl\n"
        "Total W.B.C. Count: 6500 /uL\n"
        "Platelet Count: 200 /uL\n"
    )


@pytest.fixture(scope="session")
def abnormal_report_text():
    """Report with several out-of-range values."""
    return (
        "Hemoglobin: 8.5 g/dl\n"
        "Total W.B.C. Count: 15000 /uL\n"
        "Neutrophils: 80.0 %\n"
        "Lymphocytes: 10.0 %\n"
        "Platelet Count: 90 /uL\n"
    )


@pytest.fixture(scope="session")
def abbreviated_report_text():
    """Report using short abbreviations (common in OCR output)."""
    return (
        "HB: 13.0\n"
        "RBC: 4.8\n"
        "HCT: 42.0\n"
        "MCV: 87.5\n"
        "MCH: 28.0\n"
        "WBC: 8000\n"
        "Neut%: 55.0\n"
        "Lymph%: 35.0\n"
        "Eos%: 4.0\n"
        "Mono%: 6.0\n"
        "Baso%: 0.3\n"
        "Platelet Count: 300\n"
        "MPV: 9.5\n"
        "Neut (abs): 4400\n"
        "Lymph (abs): 2800\n"
        "Eos (abs): 320\n"
        "Mono (abs): 480\n"
        "Baso (abs): 24\n"
    )


@pytest.fixture(scope="session")
def extra_spaces_report_text():
    """Report text with excessive whitespace (common OCR artefact)."""
    return (
        "Hemoglobin    :    14.0   g/dl\n"
        "Total   W.B.C.  Count   :   6000    /uL\n"
        "Platelet   Count  :  220  /uL\n"
        "Neutrophils   :  55.0   %\n"
        "Lymphocytes  :   35.0   %\n"
    )


@pytest.fixture(scope="session")
def uppercase_report_text():
    """All-caps report text."""
    return (
        "HEMOGLOBIN: 15.0 G/DL\n"
        "TOTAL W.B.C. COUNT: 9000 /UL\n"
        "PLATELET COUNT: 280 /UL\n"
        "NEUTROPHILS: 58.0 %\n"
        "LYMPHOCYTES: 32.0 %\n"
    )


@pytest.fixture(scope="session")
def empty_text():
    """Empty string — should extract nothing."""
    return ""


@pytest.fixture(scope="session")
def garbage_text():
    """Non-medical text — should extract nothing meaningful."""
    return (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
        "The quick brown fox jumps over the lazy dog.\n"
        "12345 random numbers 67890.\n"
    )


@pytest.fixture(scope="session")
def dash_separated_report_text():
    """Report using dashes as separators (another OCR variation)."""
    return (
        "Hemoglobin - 13.5\n"
        "Total W.B.C. Count - 7000\n"
        "Platelet Count - 310\n"
        "Neutrophils - 62.0\n"
        "Lymphocytes - 28.0\n"
    )


@pytest.fixture(scope="session")
def patient_info_full_text():
    """Report text with comprehensive patient demographics."""
    return (
        "MEDILAB PATHOLOGY CENTRE\n"
        "Branch: Bandra\n"
        "Contact: +91-9988776655\n"
        "\n"
        "Name: Ananya Deshmukh  Gender: Female  Age: 42\n"
        "Sample ID: 789012\n"
        "Report Date: 20-04-2025 14:00\n"
        "\n"
        "Hemoglobin: 13.0 g/dl\n"
    )


@pytest.fixture(scope="session")
def patient_info_minimal_text():
    """Report text with no patient demographics at all."""
    return (
        "Hemoglobin: 11.0 g/dl\n"
        "Platelet Count: 180000 /uL\n"
    )


@pytest.fixture(scope="session")
def columnar_report_text():
    """Simulated columnar OCR format (test names in one block, values after 'Result')."""
    return (
        "Hemoglobin\n"
        "Total R.B.C. Count\n"
        "Haematocrit (PCV/HCT)\n"
        "Mean Corpuscular Volume (M.C.V.)\n"
        "Mean Corpuscular Hb (M.C.H.)\n"
        "Total W.B.C. Count\n"
        "Neutrophils\n"
        "Lymphocytes\n"
        "Eosinophils\n"
        "Monocytes\n"
        "Basophils\n"
        "Platelet Count\n"
        "MPV\n"
        "Neutrophils (abs)\n"
        "Lymphocytes (abs)\n"
        "Eosinophils (abs)\n"
        "Monocytes (abs)\n"
        "Basophils (abs)\n"
        "\n"
        "Result\n"
        "14.0\n"
        "5.0\n"
        "43.0\n"
        "86.0\n"
        "28.0\n"
        "7000\n"
        "58.0\n"
        "32.0\n"
        "4.0\n"
        "5.0\n"
        "1.0\n"
        "260000\n"
        "9.8\n"
        "4060\n"
        "2240\n"
        "280\n"
        "350\n"
        "70\n"
        "\n"
        "Unit\n"
    )
