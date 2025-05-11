import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def test_open_redirect(url):
    payloads = [
        "https://evil.com",
        "//evil.com",
        "/\\evil.com",
        "///evil.com",
        "http://attacker.com"
    ]

    headers = {
        "User-Agent": "ShadowFox-Redirect"
    }

    for payload in payloads:
        if "FUZZ" in url:
            test_url = url.replace("FUZZ", payload)
        else:
            test_url = f"{url}?next={payload}"

        try:
            r = requests.get(test_url, headers=headers, timeout=8, allow_redirects=False)
            location = r.headers.get("Location", "")
            if location.startswith("http://") or location.startswith("https://"):
                log_to_text(f"[OPEN_REDIRECT] {test_url} -> {location}")
                severity = classify_severity(location)
                ai_trigger_if_needed("Open Redirect", test_url, payload, location, severity)
                print(f"[+] Otvoreni redirect detektovan: {test_url} -> {location}")
                return {"url": test_url, "redirect_to": location, "severity": severity}
        
        except Exception as e:
            print(f"[-] Greška: {e}")

    print("[-] Nema otvorenih redirecta.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()
    
    for url in targets:
        test_open_redirect(url)
