import os
import sys
import argparse
from dotenv import load_dotenv

# 1. Interaktivno biranje AI režima
def init_ai_mode():
    odgovor = input("Da li želiš da koristiš AI analizu? (y/n): ").strip().lower()
    if odgovor == "n":
        os.environ["DISABLE_AI"] = "1"
        print("[AI ISKLJUČEN] Radićeš bez AI analize.")
    elif odgovor == "y":
        load_dotenv()
        if os.getenv("OPENAI_API_KEY"):
            print("[AI UKLJUČEN] GPT-4o će biti korišćen za analizu.")
        else:
            print("[GREŠKA] Nema API ključa u .env fajlu.")
            sys.exit(1)
    else:
        print("Molim te odgovori sa 'y' ili 'n'.")
        sys.exit(1)

init_ai_mode()

# 2. CLI komande
parser = argparse.ArgumentParser(description="ShadowFox CLI")
parser.add_argument("--fuzz", action="store_true", help="Pokreće sve fuzz testove + AI analiza + PDF")
parser.add_argument("--summary", action="store_true", help="Prikazuje rezime iz logova")
parser.add_argument("--pdf", action="store_true", help="Samo generiše PDF iz postojećih logova")
args = parser.parse_args()

# 3. Uvoz funkcija
if args.fuzz:
    from poc_scripts.shadowfuzz_all import shadowfuzz_all

    # Učitavanje meta iz targets fajla
    with open("targets/targets.txt", "r") as f:
        targets = [url.strip() for url in f.readlines() if url.strip()]

    shadowfuzz_all(targets)


if args.summary:
    from poc_scripts.shadowscan_summary import summarize_logs
    summarize_logs()

if args.pdf:
    from poc_scripts.generate_pdf import generate_pdf_from_logs
    generate_pdf_from_logs()

# 4. Ako ništa nije prosleđeno
if not any([args.fuzz, args.summary, args.pdf]):
    print("""
ShadowFox CLI:
  --fuzz       Pokreće sve fuzz testove + analizu + PDF
  --summary    Prikazuje rezime iz logova
  --pdf        Samo generiše PDF iz postojećih logova

Primer:
  python main.py --fuzz
""")
