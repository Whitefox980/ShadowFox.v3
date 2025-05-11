import requests
from utils.log_utils import log_to_sheet, classify_severity

ID_RANGE = range(1, 5)  # Za testiranje: menja ID od 1 do 4
ID_PARAM_KEYS = ["id", "user", "account", "profile", "order"]

def load_targets(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def run_idor_scan():
    targets = load_targets("targets/targets.txt")
    for base_url in targets:
        for param in ID_PARAM_KEYS:
            for test_id in ID_RANGE:
                url = f"{base_url}?{param}={test_id}"
                try:
                    r = requests.get(url, timeout=5)
                    if r.status_code == 200 and "error" not in r.text.lower():
                        log = f"[+] Moguća IDOR ranjivost: {url}"
                        print(log)
                        severity = classify_severity(log)
                        log_to_sheet(__file__, log) + f' | Severity: {{severity}}')
                except:
                    continue

if __name__ == "__main__":
    run_idor_scan()
