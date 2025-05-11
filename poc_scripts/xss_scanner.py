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
    qs = parse_qs(parsed.query)
    new_qs = {k: payload for k in qs}
    new_query = urlencode(new_qs, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

def detect_waf(url):
    try:
        res = requests.get(url, timeout=5)
        headers = res.headers
        waf_signs = ["cloudflare", "sucuri", "akamai", "imperva", "aws", "360wzb", "wallarm", "barracuda"]
        for k, v in headers.items():
            if any(waf in v.lower() for waf in waf_signs):
                return True, f"WAF Detected: {k}: {v}"
    except:
        return False, "Greška pri detekciji WAF-a"
    return False, "Bez WAF zaštite"

def run_xss_scan():
    targets = load_targets("targets/targets.txt")

    for url in targets:
        print(f"[+] Testiram: {url}")
        waf_status, waf_info = detect_waf(url)
        print(f"[WAF] {waf_info}")

        injected_url = inject_payload(url, XSS_PAYLOAD)
        try:
            res = requests.get(injected_url, timeout=5)
            if XSS_PAYLOAD in res.text:
                rezultat = f"[!] Moguća XSS ranjivost na {url}\nWAF: {waf_info}"
                print(rezultat)
                severity = classify_severity(rezultat)
                log_to_text(__file__, rezultat + f' | Severity: {{severity}}')
            else:
                rezultat = f"[-] Nema refleksije.\nWAF: {waf_info}"
                print(rezultat)
                severity = classify_severity(rezultat)
                log_to_text(__file__, rezultat + f' | Severity: {{severity}}')
        except requests.RequestException as e:
            error = f"[X] Greška prilikom slanja zahteva ka {url}: {str(e)}"
            print(error)
            severity = classify_severity(error)
            log_to_text(__file__, error + f' | Severity: {{severity}}')

if __name__ == "__main__":
    run_xss_scan()
