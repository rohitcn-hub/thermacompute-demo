from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

def generate_pdf_report(metrics: dict, output_path: str) -> str:
    """
    Generates an executive PDF report for the thermal waste audit.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#1a365d"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor("#2d3748"),
        spaceBefore=15,
        spaceAfter=10
    )

    body_style = styles['Normal']

    elements = []

    # Title
    elements.append(Paragraph("ThermaCompute AI — Cluster Diagnostic Audit", title_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Executive Summary Box
    summary = metrics['summary']
    summary_data = [
        [
            Paragraph(f"<b>Total Dollars Wasted:</b> ${summary['total_financial_waste']:.2f}", body_style),
            Paragraph(f"<b>Throttled Hours:</b> {summary['total_throttled_hours']:.2f}h", body_style),
            Paragraph(f"<b>GPUs Affected:</b> {summary['gpus_affected']}", body_style)
        ]
    ]

    summary_table = Table(summary_data, colWidths=[2 * inch] * 3)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#edf2f7")),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor("#cbd5e0")),
        ('PADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    elements.append(Paragraph("Executive Summary", header_style))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Per-GPU Telemetry Table
    elements.append(Paragraph("Per-GPU Telemetry Summary", header_style))

    table_data = [["GPU ID", "Max Temp (°C)", "Avg Throttled Clock (MHz)", "Financial Loss ($)"]]
    for gpu in metrics['gpu_details']:
        table_data.append([
            gpu['gpu_id'],
            f"{gpu['max_temp']:.1f}",
            f"{gpu['avg_throttled_clock']:.1f}",
            f"${gpu['dollar_loss']:.2f}"
        ])

    gpu_table = Table(table_data, colWidths=[1 * inch] * 4)
    gpu_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2d3748")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white])
    ]))

    elements.append(gpu_table)
    elements.append(Spacer(1, 0.5 * inch))

    # Recommendations
    elements.append(Paragraph("Recommendations", header_style))
    reco_text = (
        "Our analysis indicates significant compute throughput loss due to thermal throttling. "
        "To eliminate these unbilled stalls, we recommend the following: <br/><br/>"
        "1. <b>Thermal Co-Scheduling:</b> Implement workload migration from hot-spots to cooler nodes dynamically.<br/>"
        "2. <b>Clock Synchronization:</b> Align GPU clock states across the cluster to prevent straggler-induced pipeline stalls.<br/>"
        "3. <b>Active Cooling Audit:</b> Investigate GPUs 2 and 5 for potential heatsink degradation or airflow obstruction."
    )
    elements.append(Paragraph(reco_text, body_style))

    doc.build(elements)
    return output_path
