from fpdf import FPDF
import datetime
import os

def generate_ai_pdf(payload, url, output, exploit, fix, severity, strategy="Unknown", agent="ShadowAgentX"):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"report_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def write_title(title):
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, title, ln=True)
        pdf.set_font("Arial", size=12)

    write_title("SHADOWFOX AI SECURITY REPORT")
    pdf.cell(200, 10, f"Timestamp: {timestamp}", ln=True)
    pdf.cell(200, 10, f"Strategy Used: {strategy}", ln=True)
    pdf.cell(200, 10, f"AgentX Source: {agent}", ln=True)
    pdf.ln(5)

    pdf.multi_cell(0, 10, f"URL: {url}")
    pdf.multi_cell(0, 10, f"Payload: {payload}")
    pdf.multi_cell(0, 10, f"\n[OUTPUT]\n{output}")
    pdf.multi_cell(0, 10, f"\n[EXPLOIT]\n{exploit}")
    pdf.multi_cell(0, 10, f"\n[FIX]\n{fix}")
    pdf.multi_cell(0, 10, f"\n[SEVERITY]: {severity}")

    path = os.path.join("reports", filename)
    pdf.output(path)

    print(f"[✓] PDF izveštaj sačuvan kao: {filename}")
    return path
