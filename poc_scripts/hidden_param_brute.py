import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from core.log_to_text import log_to_text, classify_severity
COMMON_PARAMS = [
    "debug", "admin", "test", "dev", "user", "pass", "config", "include", "file",
    "lang", "page", "dir", "path", "load", "view", "redirect", "url", "next"
]

def load_targets(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def test_param(url, param):
    try:
        response = requests.get(url, params={param: "1"}, timeout=5)
        if "error" in response.text.lower() or param in response.text:
            return True
    except:
        pass
    return False

def run_hidden_param_brute():
    targets = load_targets("targets/targets.txt")
    for url in targets:
        print(f"[•] Testiram: {url}")
        for param in COMMON_PARAMS:
            full_url = f"{url}?{param}=1"
            if test_param(url, param):
                log = f"[+] Reflektovan parametar pronađen: {param} na {full_url}"
                print(log)
                severity = classify_severity(log)
                log_to_text(__file__, log + f' | Severity: {{severity}}')

if __name__ == "__main__":
    run_hidden_param_brute()
