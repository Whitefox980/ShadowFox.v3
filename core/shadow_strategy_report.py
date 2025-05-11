from fpdf import FPDF
from core.white_shadow_advisor import generate_defensive_advice
from core.black_shadow_advisor import black_shadow_think
from io import StringIO
import datetime

def capture_stdout(func):
    import sys
    from contextlib import redirect_stdout
    temp = StringIO()
    with redirect_stdout(temp):
        func()
    return temp.getvalue()

def generate_shadow_strategy_report():
    white = capture_stdout(generate_defensive_advice)
    black = capture_stdout(black_shadow_think)

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    filename = f"shadow_strategy_report_{timestamp}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, "SHADOW STRATEGIJSKI IZVEŠTAJ", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, f"Datum: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, "\n[WHITE SHADOW ADVISOR]", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, white)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, "\n[BLACK SHADOW ADVISOR]", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, black)

    path = f"reports/{filename}"
    pdf.output(path)

    print(f"\n[✓] Shadow Strategijski PDF generisan: {path}")
