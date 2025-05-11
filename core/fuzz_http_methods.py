import requests
from logics.fuzz_ai_trigger import ai_trigger_if_needed

METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]

def fuzz_methods(url):
    print(f"\n[+] HTTP Method Fuzz test na {url}\n")

    try:
        baseline_resp = requests.get(url, timeout=5)
        baseline_len = len(baseline_resp.text)
    except:
        baseline_len = 0

    for method in METHODS:
        try:
            r = requests.request(method, url, timeout=5)
            size = len(r.text) if method != "HEAD" else 0
            diff = size - baseline_len

            print(f"{method:7} => [{r.status_code}] Δ {diff:+4} B")

            ai_trigger_if_needed(method, r.text, url, reflected=False, size_diff=diff)

        except Exception as e:
            print(f"{method:7} => [ERR] {e}")
