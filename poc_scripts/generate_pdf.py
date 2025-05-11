from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime

def create_summary_pdf(summary, output="reports/shadow_summary.pdf"):
    c = canvas.Canvas(output, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "ShadowFox - Rezime Skeniranja")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Datum: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 40

    for vuln, count in summary.items():
        if count > 0:
            c.drawString(60, y, f"{vuln}: {count}")
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50

    c.save()
    print(f"[+] PDF izveštaj sačuvan kao: {output}")
