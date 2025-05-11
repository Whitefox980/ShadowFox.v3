import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def discover_params(url, wordlist=None):
    if wordlist is None:
        wordlist = [
            "debug", "test", "admin", "submit", "role", "access", "auth",
            "config", "cmd", "action", "search", "validate"
        ]

    headers = {"User-Agent": "ShadowFox-ParamDiscovery"}
    results = []

    for param in wordlist:
        test_url = f"{url}?{param}=test"
        try:
            res = requests.get(test_url, headers=headers, timeout=6)
            if res.status_code == 200 and "error" not in res.text.lower():
                results.append({
                    "url": test_url,
                    "param": param,
                    "content": res.text,
                    "status": res.status_code
                })
                print(f"[+] Parametar otkriven: {param}")
        except Exception as e:
            print(f"[-] Greška kod {test_url}: {e}")

    return results
