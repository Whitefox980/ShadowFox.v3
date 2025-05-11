import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def brute_hidden_params(url):
    common_params = [
        "debug", "admin", "access", "view", "role", "user",
        "test", "auth", "mode", "config", "override", "action"
    ]

    headers = {"User-Agent": "ShadowFox-HiddenParamBrute"}
    results = []

    for param in common_params:
        for value in ["1", "true", "yes", "on", "admin"]:
            test_url = f"{url}?{param}={value}"
            try:
                res = requests.get(test_url, headers=headers, timeout=6)
                if res.status_code == 200 and "login" not in res.text.lower():
                    results.append({
                        "url": test_url,
                        "param": f"{param}={value}",
                        "content": res.text,
                        "status": res.status_code
                    })
                    print(f"[+] Hidden param: {param}={value}")
            except Exception as e:
                print(f"[-] Greška kod {test_url}: {e}")

    return results
if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()

    for url in targets:
        brute_hidden_params(url)
