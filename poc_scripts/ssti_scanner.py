import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from core.log_to_text import log_to_text, classify_severity
SSTI_PAYLOAD = "{{7*7}}"
SSTI_EVAL = "49"

def load_targets(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def run_ssti_scan():
    targets = load_targets("targets/targets.txt")
    for base_url in targets:
        test_url = f"{base_url}?input={SSTI_PAYLOAD}"
        try:
            r = requests.get(test_url, timeout=5)
            if SSTI_EVAL in r.text:
                log = f"[+] SSTI detektovan: {test_url}"
                print(log)
                severity = classify_severity(log)
                log_to_text(__file__, log + f' | Severity: {{severity}}')
            else:
                print(f"[-] Nema SSTI: {test_url}")
        except:
            continue

if __name__ == "__main__":
    run_ssti_scan()
