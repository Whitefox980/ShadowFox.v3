import requests
from logics.ai_tools import suggest_exploit, suggest_fix, classify_severity
from logics.generate_pdf import save_ai_report_to_pdf

def run_custom_scan(url, payloads):
    print(f"\n[+] CUSTOM FUZZ na {url}")
    try:
        baseline = requests.get(url.replace("FUZZ", "base"), timeout=5).text
    except:
        baseline = ""

    for i, payload in enumerate(payloads, 1):
        test_url = url.replace("FUZZ", payload)
        try:
            r = requests.get(test_url, timeout=5)
            reflected = payload in r.text
            diff = len(r.text) - len(baseline)
            print(f"{i:02d}. Δ {diff:+4} | {test_url}")

            if reflected:
                print("   [!!!] REFLEKSIJA! AI pokreće:")
                exploit = suggest_exploit(r.text)
                fix = suggest_fix(r.text)
                severity = classify_severity(r.text)

                summary = f"[CUSTOM REFLECT]\nPayload: {payload}\nURL: {test_url}\n\n[EXPLOIT]\n{exploit}\n\n[FIX]\n{fix}\n\n[SEVERITY]: {severity}"
                save_ai_report_to_pdf(summary, site=test_url)

        except Exception as e:
            print(f"{i:02d}. [ERR] {test_url} => {e}")
