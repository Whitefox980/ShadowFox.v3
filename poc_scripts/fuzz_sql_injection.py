import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.sql_payload_mutator import generate_sql_payloads
from poc_scripts.log_to_text import log_to_text
from logics.fuzz_ai_trigger import ai_trigger_if_needed
from tools.auto_add_severity import classify_severity
from utils.use_ai_flag import USE_AI

def fuzz_sql_injection(url):
    base_param = "id"
    payloads = generate_sql_payloads(url)

    headers = {
        "User-Agent": "ShadowFox-SQLiFuzz"
    }

    for payload in payloads:
        test_url = f"{url}?{base_param}={payload}"
        try:
            res = requests.get(test_url, headers=headers, timeout=6)
            if res.status_code == 200 and ("sql" in res.text.lower() or "syntax" in res.text.lower() or "error" in res.text.lower()):
                log_to_text("[FUZZ_SQLI]", f"{test_url}")
                severity = classify_severity(res.text)
                ai_trigger_if_needed("SQL Injection", test_url, payload, res.text, severity)
                print(f"[+] SQLi uspešan na: {test_url}")
        except Exception as e:
            print(f"[-] Greška kod {test_url}: {e}")

    print("[-] SQL Injection fuzz završen.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()

    for url in urls:
        fuzz_sql_injection(url)
