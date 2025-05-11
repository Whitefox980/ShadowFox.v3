import requests
from logics.fuzz_gen import fuzz_payload
from logics.ai_tools import suggest_exploit, suggest_fix, classify_severity
from logics.generate_pdf import save_ai_report_to_pdf

def run_reflect_scan(url, base_payload):
    print(f"\n[+] TURBO REFLECT Scan on {url}")
    mutations = fuzz_payload(base_payload)

    try:
        baseline = requests.get(url.replace("FUZZ", "base"), timeout=5).text
    except:
        baseline = ""

    for i, m in enumerate(mutations, 1):
        test_url = url.replace("FUZZ", m)
        try:
            r = requests.get(test_url, timeout=5)
            reflected = m in r.text
            diff = len(r.text) - len(baseline)
            print(f"{i:02d}. Δ {diff:+4} | {test_url}")

            if reflected:
                print("   [!!!] REFLECTED Payload detektovan! AI ANALIZA:")
                exploit = suggest_exploit(r.text)
                fix = suggest_fix(r.text)
                severity = classify_severity(r.text)

                summary = f"[TURBO REFLECT]\nPayload: {m}\nURL: {test_url}\n\n[EXPLOIT]\n{exploit}\n\n[FIX]\n{fix}\n\n[SEVERITY]: {severity}"
                save_ai_report_to_pdf(summary, site=test_url)

        except Exception as e:
            print(f"{i:02d}. [ERR] {test_url} => {e}")
