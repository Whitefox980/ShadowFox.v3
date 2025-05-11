import requests, time
from logics.fuzz_gen import fuzz_payload
from logics.ai_tools import suggest_exploit, suggest_fix, classify_severity
from logics.generate_pdf import save_ai_report_to_pdf

DNSLOG_URL = "https://dnslog.cn/getrecords.php"  # koristiš svoj ako imaš

def dns_triggered():
    try:
        r = requests.get(DNSLOG_URL, timeout=5)
        return "No record" not in r.text
    except:
        return False

def ghost_hunt(url, base_payload):
    print(f"\n[☠] ShadowFox Ghost Protocol aktiviran na {url}")
    mutations = fuzz_payload(base_payload)

    try:
        baseline = requests.get(url.replace("FUZZ", "base"), timeout=5).text
    except:
        baseline = ""

    for i, m in enumerate(mutations, 1):
        test_url = url.replace("FUZZ", m)
        try:
            r = requests.get(test_url, timeout=5)
            diff = len(r.text) - len(baseline)
            reflected = m in r.text
            print(f"{i:02d}. Δ {diff:+4} | Reflektovano: {'DA' if reflected else 'ne'} | {test_url}")

            # Daj mu fore za DNS log
            time.sleep(2)
            dns = dns_triggered()

            if reflected or dns:
                print("   [✓] Aktivnost detektovana! AI analiza kreće...")
                exploit = suggest_exploit(r.text)
                fix = suggest_fix(r.text)
                severity = classify_severity(r.text)

                summary = f"[GHOST-MODE]\nPayload: {m}\nURL: {test_url}\nReflektovano: {reflected}\nDNS: {dns}\n\n[SEVERITY]: {severity}\n\n[EXPLOIT]\n{exploit}\n\n[FIX]\n{fix}"
                save_ai_report_to_pdf(summary, site=test_url)

        except Exception as e:
            print(f"[ERR] {test_url} => {e}")
