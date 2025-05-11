import json
import os
from datetime import datetime

EXPORT_DIR = "exports"
LOG_FILE = "results_log.json"

def export_to_bugcrowd_format():
    if not os.path.exists(LOG_FILE):
        print("[!] Nema log fajla.")
        return

    os.makedirs(EXPORT_DIR, exist_ok=True)

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    for i, r in enumerate(data):
        filename = f"{EXPORT_DIR}/report_{i+1}_{r['tool']}.txt"
        with open(filename, "w") as out:
            out.write(f"Title: {r['tool'].upper()} on {r['target']}\n")
            out.write(f"Target: {r['target']}\n")
            out.write(f"Severity: {r['severity']}\n")
            out.write(f"Status: {r['status']}\n")
            out.write(f"Date: {r['timestamp']}\n\n")
            out.write("Steps to Reproduce:\n")
            out.write("(1) Navigate to target\n(2) Trigger payload\n\n")
            out.write("Observed Output:\n")
            out.write(r['output'][:1000] + "\n\n")
            out.write("Expected Behavior:\nSystem should sanitize input / reject malicious data.\n\n")
            out.write("Fix Recommendation:\nUse input validation, WAF, or patch vulnerable logic.\n")

    print(f"[✓] Eksportovano {len(data)} izveštaja u {EXPORT_DIR}/")
