import requests
import json
from logics.fuzz_ai_trigger import ai_trigger_if_needed

PAYLOADS = [
    {"admin": True},
    {"debug": True},
    {"isSuperuser": 1},
    {"role": "root"},
    {"user": "admin", "access": "all"},
    {"bypass": True},
    {"active": 1}
]

def fuzz_json(url):
    print(f"\n[+] JSON Body Fuzz test na {url}\n")
    headers = {"Content-Type": "application/json"}

    try:
        baseline_resp = requests.post(url, headers=headers, data=json.dumps({"baseline": True}), timeout=5)
        baseline_len = len(baseline_resp.text)
    except:
        baseline_len = 0

    for i, data in enumerate(PAYLOADS, 1):
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data), timeout=5)
            diff = len(r.text) - baseline_len
            payload_str = json.dumps(data)
            print(f"{i:02d}. [{r.status_code}] {payload_str} | Δ {diff:+4} B")

            ai_trigger_if_needed(payload_str, r.text, url, reflected=False, size_diff=diff)

        except Exception as e:
            print(f"[ERR] {data} => {e}")
