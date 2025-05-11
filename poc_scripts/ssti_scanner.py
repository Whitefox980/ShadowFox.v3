import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def test_ssti(url):
    payloads = [
        "{{7*7}}",        # Jinja2
        "${7*7}",         # Velocity
        "#{7*7}",         # Twig
        "<%= 7*7 %>",     # ERB
        "${{7*7}}"
    ]

    headers = {
        "User-Agent": "ShadowFox-SSTI"
    }

    for payload in payloads:
        if "FUZZ" in url:
            test_url = url.replace("FUZZ", payload)
        else:
            test_url = f"{url}?input={payload}"

        try:
            res = requests.get(test_url, headers=headers, timeout=8)
            if "49" in res.text or "error" in res.text.lower():
                log_to_text(f"[SSTI] {test_url} -> {payload}")
                severity = classify_severity(res.text)
                ai_trigger_if_needed("SSTI", test_url, payload, res.text, severity)
                print(f"[+] SSTI Detekcija: {test_url}")
                return {"url": test_url, "payload": payload, "severity": severity}
        
        except Exception as e:
            print(f"[-] Greška: {e}")
    
    print("[-] SSTI nije detektovan.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()
    
    for url in targets:
        test_ssti(url)
