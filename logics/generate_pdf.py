from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def save_ai_report_to_pdf(analysis_text, output_path="reports/ai_report.pdf", site="N/A"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 50, f"AI Bezbednosna Analiza — {site}")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 70, f"Datum: {now}")

    text_object = c.beginText(40, height - 100)
    text_object.setFont("Helvetica", 10)

    for line in analysis_text.split("\n"):
        for subline in split_long_lines(line, 90):
            text_object.textLine(subline)

    c.drawText(text_object)
    c.save()

def split_long_lines(text, max_length):
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 <= max_length:
            current += " " + word
        else:
            lines.append(current.strip())
            current = word
    lines.append(current.strip())
    return lines
