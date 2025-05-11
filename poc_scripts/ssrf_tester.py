import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.log_utils import log_to_sheet, classify_severity

SSRF_PROBE = "http://127.0.0.1"  # Možeš koristiti i custom listener ako želiš

def test_ssrf(base_url):
    parsed = urlparse(base_url)
    query = parse_qs(parsed.query)

    for key in query:
        original = query[key][0]
        query[key] = [SSRF_PROBE]
        new_query = urlencode(query, doseq=True)
        test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', new_query, ''))

        try:
            r = requests.get(test_url, timeout=5)
            if r.status_code == 200:
                msg = f"[!] Moguća SSRF refleksija: {test_url}"
                print(msg)
                severity = classify_severity(msg)
                log_to_sheet(__file__, msg) + f' | Severity: {{severity}}')
        except Exception as e:
            print(f"[-] Greška SSRF za {test_url}: {e}")

def run_ssrf_scan():
    with open("targets/targets.txt", "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    for url in targets:
        print(f"[~] Testiram SSRF na: {url}")
        test_ssrf(url)

if __name__ == "__main__":
    run_ssrf_scan()
