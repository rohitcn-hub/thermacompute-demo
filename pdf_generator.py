from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

class PDFGenerator:
    def __init__(self):
        # Enterprise Palette
        self.colors = {
            'navy': HexColor('#0F172A'),
            'cyan': HexColor('#0284C7'),
            'slate': HexColor('#1E293B'),
            'white': HexColor('#FFFFFF'),
            'light_slate': HexColor('#F1F5F9')
        }

    def generate_report(self, metrics, filename="audit_report.pdf"):
        """
        Generates a 5-page executive thermal audit PDF.
        :param metrics: Dictionary containing:
            - client_name
            - total_gpus
            - peak_temp
            - throttled_gpus
            - monthly_waste_usd
        """
        c = canvas.Canvas(filename, pagesize=LETTER)
        width, height = LETTER

        # Page 1: Executive Cover Page
        self._draw_cover_page(c, width, height, metrics)
        c.showPage()

        # Page 2: GPU Telemetry & Thermal Throttling
        self._draw_telemetry_page(c, width, height, metrics)
        c.showPage()

        # Page 3: CapEx & Hardware Inefficiency
        self._draw_capex_page(c, width, height, metrics)
        c.showPage()

        # Page 4: Dual-Brain Architecture
        self._draw_architecture_page(c, width, height)
        c.showPage()

        # Page 5: Action Plan & CTA
        self._draw_cta_page(c, width, height)
        c.showPage()

        c.save()
        return filename

    def _draw_header_footer(self, c, width, height):
        # Top accent bar
        c.setFillColor(self.colors['navy'])
        c.rect(0, height - 0.25*inch, width, 0.25*inch, fill=1, stroke=0)

        # Footer
        c.setFillColor(self.colors['slate'])
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, 0.5*inch, "ThermaCompute AI Confidential - Thermal Audit Report")

    def _draw_cover_page(self, c, width, height, metrics):
        # Background accent
        c.setFillColor(self.colors['navy'])
        c.rect(0, height*0.6, width, height*0.4, fill=1, stroke=0)

        # Title
        c.setFillColor(self.colors['white'])
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(width/2, height*0.75, "EXECUTIVE THERMAL AUDIT")

        c.setFont("Helvetica", 18)
        c.drawCentredString(width/2, height*0.68, f"Prepared for: {metrics['client_name']}")

        # Financial Waste Disclosure
        c.setFillColor(self.colors['navy'])
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height*0.4, "MONTHLY FINANCIAL WASTE")

        c.setFillColor(self.colors['cyan'])
        c.setFont("Helvetica-Bold", 48)
        c.drawCentredString(width/2, height*0.3, f"${metrics['monthly_waste_usd']:,.2f}")

        c.setFillColor(self.colors['slate'])
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height*0.22, "Due to thermal throttling and clock downclocking events.")

        self._draw_header_footer(c, width, height)

    def _draw_telemetry_page(self, c, width, height, metrics):
        self._draw_header_footer(c, width, height)

        c.setFillColor(self.colors['navy'])
        c.setFont("Helvetica-Bold", 20)
        c.drawString(1*inch, height - 1*inch, "GPU Telemetry & Thermal Throttling Analysis")

        c.setFillColor(self.colors['slate'])
        c.setFont("Helvetica", 12)
        text_y = height - 1.5*inch

        # Metric blocks
        metrics_to_show = [
            f"Total GPUs Monitored: {metrics['total_gpus']}",
            f"Peak Junction Temperature: {metrics['peak_temp']}°C",
            f"GPUs Experiencing Throttling: {metrics['throttled_gpus']}",
            f"Thermal Status: {'CRITICAL' if metrics['peak_temp'] > 85 else 'OPTIMAL'}"
        ]

        for line in metrics_to_show:
            c.drawString(1*inch, text_y, line)
            text_y -= 0.3*inch

        # Analysis box
        c.setFillColor(self.colors['light_slate'])
        c.rect(1*inch, text_y - 0.5*inch, width - 2*inch, 2*inch, fill=1, stroke=0)

        c.setFillColor(self.colors['navy'])
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1.2*inch, text_y + 1.2*inch, "Analysis:")

        c.setFillColor(self.colors['slate'])
        c.setFont("Helvetica", 11)
        analysis = (
            f"The data indicates that {metrics['throttled_gpus']} out of {metrics['total_gpus']} GPUs "
            f"have exceeded the thermal threshold, causing the hardware to automatically downclock "
            f"to prevent permanent damage. This reduction in clock speed directly translates to "
            f"lost compute cycles and increased training/inference time."
        )

        # Simple word wrap for the analysis
        text_obj = c.beginText(1.2*inch, text_y + 0.9*inch)
        text_obj.setFont("Helvetica", 11)
        text_obj.setLeading(14)

        # Manual wrapping for simplicity
        words = analysis.split(' ')
        line = ""
        for word in words:
            if len(line + word) < 80:
                line += word + " "
            else:
                text_obj.textLine(line)
                line = word + " "
        text_obj.textLine(line)
        c.drawText(text_obj)

    def _draw_capex_page(self, c, width, height, metrics):
        self._draw_header_footer(c, width, height)

        c.setFillColor(self.colors['navy'])
        c.setFont("Helvetica-Bold", 20)
        c.drawString(1*inch, height - 1*inch, "CapEx & Hardware Inefficiency Assessment")

        c.setFillColor(self.colors['slate'])
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 1.4*inch, "Thermal throttling doesn't just cost time; it creates 'Ghost Hardware'.")

        # Calculation for "Idle GPU equivalent"
        # Assume a throttled GPU loses 20% efficiency
        efficiency_loss = (metrics['throttled_gpus'] * 0.2)

        c.setFillColor(self.colors['cyan'])
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 2*inch, f"Equivalent Idle Capacity: {efficiency_loss:.2f} GPUs")

        c.setFillColor(self.colors['slate'])
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 2.3*inch, "This means you are paying for the power, cooling, and rack space")
        c.drawString(1*inch, height - 2.5*inch, "of hardware that is operating significantly below its rated capacity.")

    def _draw_architecture_page(self, c, width, height):
        self._draw_header_footer(c, width, height)

        c.setFillColor(self.colors['navy'])
        c.setFont("Helvetica-Bold", 20)
        c.drawString(1*inch, height - 1*inch, "ThermaCompute Dual-Brain Architecture")

        # System 1
        c.setFillColor(self.colors['light_slate'])
        c.rect(1*inch, height - 3*inch, 3*inch, 1.5*inch, fill=1, stroke=0)
        c.setFillColor(self.colors['navy'])
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1.2*inch, height - 2.2*inch, "System 1: The Reflex")
        c.setFillColor(self.colors['slate'])
        c.setFont("Helvetica", 10)
        c.drawString(1.2*inch, height - 2.5*inch, "Real-time telemetry monitoring.")
        c.drawString(1.2*inch, height - 2.7*inch, "Instant throttling detection.")

        # System 2
        c.setFillColor(self.colors['light_slate'])
        c.rect(4.5*inch, height - 3*inch, 3*inch, 1.5*inch, fill=1, stroke=0)
        c.setFillColor(self.colors['navy'])
        c.setFont("Helvetica-Bold", 14)
        c.drawString(4.7*inch, height - 2.2*inch, "System 2: The Predictive")
        c.setFillColor(self.colors['slate'])
        c.setFont("Helvetica", 10)
        c.drawString(4.7*inch, height - 2.5*inch, "Pattern recognition over time.")
        c.drawString(4.7*inch, height - 2.7*inch, "Proactive thermal load shifting.")

    def _draw_cta_page(self, c, width, height):
        self._draw_header_footer(c, width, height)

        c.setFillColor(self.colors['navy'])
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, height - 1*inch, "Action Plan")

        c.setFillColor(self.colors['slate'])
        c.setFont("Helvetica", 12)
        steps = [
            "1. Immediate thermal audit of all H100/A100 clusters.",
            "2. Implementation of the ThermaCompute Reflex layer.",
            "3. Transition to Predictive Load Balancing.",
            "4. Recalibration of cooling set-points."
        ]

        y = height - 1.6*inch
        for step in steps:
            c.drawString(1*inch, y, step)
            y -= 0.3*inch

        # CTA Box
        c.setFillColor(self.colors['navy'])
        c.rect(1*inch, y - 1*inch, width - 2*inch, 2*inch, fill=1, stroke=0)

        c.setFillColor(self.colors['white'])
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, y - 0.4*inch, "Join Batch 1 Implementation")

        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, y - 0.7*inch, "Secure your seat for the initial rollout.")

        c.setFillColor(self.colors['cyan'])
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width/2, y - 1.1*inch, "$30 Reservation Fee")

        # Stripe Link (Simulated as a blue underline text)
        c.setFillColor(self.colors['white'])
        c.setFont("Helvetica", 10)
        link_text = "https://buy.stripe.com/thermacompute_30"
        c.drawCentredString(width/2, y - 1.4*inch, link_text)
        c.line(width/2 - 80, y - 1.43*inch, width/2 + 80, y - 1.43*inch)

if __name__ == "__main__":
    # Quick test run
    gen = PDFGenerator()
    metrics = {
        "client_name": "Enterprise AI Corp",
        "total_gpus": 128,
        "peak_temp": 92,
        "throttled_gpus": 42,
        "monthly_waste_usd": 14700.00
    }
    gen.generate_report(metrics)
    print("Report generated: audit_report.pdf")
