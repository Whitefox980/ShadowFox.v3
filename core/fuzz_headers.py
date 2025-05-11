import requests
from logics.fuzz_ai_trigger import ai_trigger_if_needed

FUZZ_HEADERS = {
    "User-Agent": ["evil-agent", "XSS-Scanner", "<script>1</script>"],
    "Referer": ["http://evil.com", "http://localhost"],
    "X-Forwarded-For": ["127.0.0.1", "0.0.0.0", "::1"],
    "Origin": ["null", "http://evil.org"],
    "Host": ["localhost", "127.0.0.1"],
    "Cookie": ["admin=true", "debug=1"]
}

def fuzz_headers(url):
    print(f"\n[+] Header Fuzz test na {url}\n")
    try:
        baseline_resp = requests.get(url, timeout=5)
        baseline_len = len(baseline_resp.text)
    except:
        baseline_len = 0

    for header, values in FUZZ_HEADERS.items():
        for val in values:
            try:
                r = requests.get(url, headers={header: val}, timeout=5)
                diff = len(r.text) - baseline_len
                reflected = val in r.text

                print(f"[{r.status_code}] {header}: {val} | Δ {diff:+4} B | Reflektovan: {'DA' if reflected else 'ne'}")

                ai_trigger_if_needed(val, r.text, url, reflected, diff)

            except Exception as e:
                print(f"[ERR] {header}: {val} => {e}")
