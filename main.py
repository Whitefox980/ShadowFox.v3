import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'poc_scripts')))

from shadowfuzz_all import shadowfuzz_all
from shadowscan_summary import summarize_logs
from shadow_log_center import generate_ui
from generate_pdf import create_summary_pdf

def load_targets():
    with open("targets/targets.txt", "r") as f:
        return f.read().splitlines()

def main():
    args = sys.argv[1:]
    targets = load_targets()

    if "--fuzz" in args:
        shadowfuzz_all(targets)
    elif "--summary" in args:
        summary = summarize_logs()
        generate_ui(summary)
    elif "--pdf" in args:
        summary = summarize_logs()
        create_summary_pdf(summary)
    elif "--recon" in args:
        from shadowrecon_all import shadowrecon_all
        shadowrecon_all(targets)
    else:
        print("""
ShadowFox CLI:
  --fuzz       Pokreće sve fuzz testove + analizu + PDF
  --summary    Prikazuje rezime iz logova
  --pdf        Samo generiše PDF iz postojećih logova

Primer:
  python main.py --fuzz
""")

if __name__ == "__main__":
    main()
