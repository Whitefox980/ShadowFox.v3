import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from urllib.parse import urlparse, urlunparse
from core.log_to_text import log_to_text, classify_severity
COMMON_PARAMS = ["id", "page", "user", "ref", "lang", "q", "search", "file", "redirect", "url"]

def discover_params(base_url):
    parsed = urlparse(base_url)
    vulnerable = []

    print(f"[+] Pokušavam GET parametre na: {base_url}")

    for param in COMMON_PARAMS:
        url = f"{base_url}?{param}=test"
        try:
            r = requests.get(url, timeout=5)
            if "test" in r.text.lower():
                print(f"[!] Refleksija za parametar: {param}")
                vulnerable.append(param)
        except:
            pass

    if vulnerable:
        summary = f"[!] Otkriveni reflektovani parametri: {', '.join(vulnerable)} na {base_url}"
    else:
        summary = f"[-] Nema otkrivenih reflektovanih GET parametara za {base_url}"

    print(summary)
    severity = classify_severity(summary)
    log_to_text(__file__, summary + f' | Severity: {{severity}}')

if __name__ == "__main__":
    with open("targets/targets.txt") as f:
        urls = [line.strip() for line in f if line.strip()]
        for u in urls:
            discover_params(u)
