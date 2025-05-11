import requests
from logics.fuzz_ai_trigger import ai_trigger_if_needed

SPLIT_PAYLOADS = [
    "1&admin=true",
    "value#token=abc123",
    "test;debug=true",
    "x=1&x=2",
    "root&role=admin",
    "id=1#auth=1"
]

def fuzz_param_split(url):
    if "FUZZ" not in url:
        print("[x] URL mora sadržati 'FUZZ'")
        return

    print(f"\n[+] Param Split Fuzz na {url}\n")

    try:
        baseline_resp = requests.get(url.replace("FUZZ", "base"), timeout=5)
        baseline_len = len(baseline_resp.text)
    except:
        baseline_len = 0

    for i, payload in enumerate(SPLIT_PAYLOADS, 1):
        test_url = url.replace("FUZZ", payload)
        try:
            r = requests.get(test_url, timeout=5)
            diff = len(r.text) - baseline_len
            reflected = payload in r.text

            print(f"{i:02d}. [{r.status_code}] {payload} | Δ {diff:+4} B | Reflektovan: {'DA' if reflected else 'ne'}")

            ai_trigger_if_needed(payload, r.text, test_url, reflected, diff)

        except Exception as e:
            print(f"[ERR] {payload} => {e}")
