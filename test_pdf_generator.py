import pytest
import os
from pdf_generator import PDFGenerator

def test_pdf_generation_success():
    """Verifies that the PDF is created, non-empty, and has a valid PDF header."""
    gen = PDFGenerator()
    metrics = {
        "client_name": "Test Client",
        "total_gpus": 10,
        "peak_temp": 90,
        "throttled_gpus": 5,
        "monthly_waste_usd": 500.00
    }
    filename = "audit_report.pdf"

    # Ensure clean start
    if os.path.exists(filename):
        os.remove(filename)

    gen.generate_report(metrics, filename=filename)

    # Check if file exists
    assert os.path.exists(filename)

    # Check if file is non-empty
    assert os.path.getsize(filename) > 0

    # Check for PDF header (%PDF-)
    with open(filename, 'rb') as f:
        header = f.read(4)
        assert header == b'%PDF'

def test_pdf_different_metrics():
    """Verifies the generator doesn't crash with different input values."""
    gen = PDFGenerator()
    metrics = {
        "client_name": "Minimal Client",
        "total_gpus": 1,
        "peak_temp": 70,
        "throttled_gpus": 0,
        "monthly_waste_usd": 0.00
    }
    filename = "audit_report_min.pdf"

    gen.generate_report(metrics, filename=filename)
    assert os.path.exists(filename)

    os.remove(filename)
