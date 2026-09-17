from backend.analyzer import analyze_dcgm
from backend.report_gen import generate_pdf_report
import os

def verify():
    csv_path = "sample_dcgm_logs.csv"
    pdf_path = "thermal_waste_audit.pdf"

    if not os.path.exists(csv_path):
        print("Error: Sample CSV not found!")
        return False

    print("Analyzing logs...")
    metrics = analyze_dcgm(csv_path)
    print(f"Metrics: {metrics['summary']}")

    print("Generating report...")
    generate_pdf_report(metrics, pdf_path)

    if os.path.exists(pdf_path):
        print("Success: PDF report generated!")
        return True
    else:
        print("Error: PDF report not generated!")
        return False

if __name__ == "__main__":
    verify()
