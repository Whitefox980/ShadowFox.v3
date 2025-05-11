import os
import sys
import re
import openai
from dotenv import load_dotenv
sys.path.append(os.path.abspath("core/ext_libs"))

from pypdf._reader import PdfReader

# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_summary_data():
    summaries = []
    for fname in os.listdir("reports"):
        if not fname.endswith(".pdf"):
            continue
        path = os.path.join("reports", fname)
        try:
            with open(path, "rb") as f:
                reader = PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""

                payload = re.search(r"Payload:\s*(.*)", text)
                severity = re.search(r"SEVERITY:\s*(.*)", text)
                fix = re.search(r"FIX\n(.*?\n)", text, re.DOTALL)

                summaries.append({
                    "file": fname,
                    "payload": payload.group(1) if payload else "N/A",
                    "severity": severity.group(1) if severity else "N/A",
                    "fix": fix.group(1).strip() if fix else "N/A"
                })
        except Exception:
            continue
    return summaries

def generate_defensive_advice():
    data = extract_summary_data()
    if not data:
        print("[x] Nema PDF izveštaja za analizu.")
        return

    prompt = (
        "Na osnovu sledećih bezbednosnih AI izveštaja (ranjivosti, payload-i, fix predlozi), "
        "savetuj kako poboljšati sistemsku bezbednost u celini.\n\n"
        f"{data}\n\n"
        "Cilj: zaštititi aplikaciju od ponovljenih napada, ojačati validaciju, i zatvoriti slične propuste u budućnosti.\n"
        "Vrati konkretne savete u tačkama."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    print("\n[WhiteShadowAdvisor AI SAVET]:\n")
    print(response.choices[0].message.content.strip())
