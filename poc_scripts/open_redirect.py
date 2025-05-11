import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from urllib.parse import urlencode
from core.log_to_text import log_to_text, classify_severity

REDIRECT_PAYLOADS = [
    "https://evil.com",
    "//evil.com",
    "/\\evil.com",
    "https://google.com@evil.com",
]

def test_open_redirect(base_url):
    for param in ["url", "next", "redirect", "redirect_url", "continue"]:
        for payload in REDIRECT_PAYLOADS:
            full_url = f"{base_url}?{urlencode({param: payload})}"
            try:
                response = requests.get(full_url, allow_redirects=False, timeout=5)
                location = response.headers.get("Location", "")
                if "evil.com" in location:
                    print(f"[!] Mogući OPEN REDIRECT: {full_url} => {location}")
                    severity = classify_severity(f"OPEN REDIRECT: {full_url} => {location}")
                    log_to_text(__file__, f"OPEN REDIRECT: {full_url} => {location}" + f' | Severity: {{severity}}')
            except Exception as e:
                print(f"[-] Greška: {e} za {full_url}")

def run_open_redirect():
    print("[~] Pokrećem OPEN REDIRECT test...")
    targets = [
        "http://testphp.vulnweb.com",  # dodaj ciljeve
    ]
    for target in targets:
        test_open_redirect(target)

if __name__ == "__main__":
    run_open_redirect()
