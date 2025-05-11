import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def test_idor(base_url, param="id", start=1, end=5):
    headers = {
        "User-Agent": "ShadowFox-IDOR-Tester"
    }

    last_response = ""
    for i in range(start, end + 1):
        url = f"{base_url}?{param}={i}"
        try:
            res = requests.get(url, headers=headers, timeout=6)
            if res.status_code == 200 and res.text != last_response:
                print(f"[+] Moguća IDOR ranjivost za {param}={i}")
                log_to_text(f"[IDOR] {url}")
                severity = classify_severity(res.text)
                ai_trigger_if_needed("IDOR", url, f"{param}={i}", res.text, severity)
                last_response = res.text
        except Exception as e:
            print(f"[-] Greška: {e}")

    print("[-] Testiranje IDOR završeno.")

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()

    for base in urls:
        test_idor(base)
