import json
import os
from datetime import datetime

EXPORT_DIR = "exports/hackerone"
LOG_FILE = "results_log.json"

def export_to_hackerone():
    if not os.path.exists(LOG_FILE):
        print("[!] Nema log fajla.")
        return

    os.makedirs(EXPORT_DIR, exist_ok=True)

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    for i, r in enumerate(data):
        filename = f"{EXPORT_DIR}/h1_{i+1}_{r['tool']}.md"
        with open(filename, "w", encoding="utf-8") as out:
            out.write(f"# [{r['tool'].upper()}] Vulnerability on {r['target']}\n\n")
            out.write(f"**Severity:** {r['severity'].capitalize()}\n")
            out.write(f"**Tool:** {r['tool']}\n")
            out.write(f"**Date:** {r['timestamp']}\n\n")

            out.write("## Summary\n")
            out.write(f"A vulnerability was found using `{r['tool']}` on `{r['target']}`.\n\n")

            out.write("## Steps To Reproduce\n")
            out.write("1. Open browser or tool.\n")
            out.write("2. Navigate to the target.\n")
            out.write("3. Trigger the payload.\n\n")

            out.write("## Supporting Material/References\n")
            out.write("```\n")
            out.write(r['output'][:1000])
            out.write("\n```\n\n")

            out.write("## Impact\n")
            out.write(f"This issue may allow attackers to abuse {r['tool']} logic and cause unexpected behavior.\n")

    print(f"[✓] HackerOne izveštaji generisani: {EXPORT_DIR}/")
