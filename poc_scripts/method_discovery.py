import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def discover_methods(url):
    methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "TRACE", "CONNECT", "PATCH"]
    headers = {"User-Agent": "ShadowFox-MethodDiscovery"}
    results = []

    for method in methods:
        try:
            res = requests.request(method, url, headers=headers, timeout=6)
            if res.status_code < 400:
                results.append({
                    "url": url,
                    "param": method,
                    "content": res.text,
                    "status": res.status_code
                })
                print(f"[+] HTTP metoda dozvoljena: {method} ({res.status_code})")
        except Exception as e:
            print(f"[-] {method} greška: {e}")

    return results
if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()

    for url in urls:
        discover_methods(url)
