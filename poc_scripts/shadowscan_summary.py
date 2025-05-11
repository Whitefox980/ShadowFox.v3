import os
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text

LOG_DIR = "logs"
pattern_map = {
    "SQLi": r"SQL(I|I_POC)?",
    "XSS": r"XSS(_POC)?",
    "LFI": r"LFI(-RFI)?",
    "RCE": r"RCE",
    "SSTI": r"SSTI",
    "SSRF": r"SSRF",
    "IDOR": r"IDOR",
    "Open Redirect": r"OPEN_REDIRECT(_POC)?",
    "Auth Bypass": r"AUTH-BYPASS",
    "Param Discovery": r"PARAM_DISCOVERY",
    "Hidden Param": r"HIDDEN_PARAM",
    "Dir Brute": r"DIR_BRUTE",
    "HTTP Method": r"METHOD",
    "Fuzz Split": r"FUZZ_PARAM_SPLITTER",
    "Fuzz JSON": r"FUZZ_JSON_BODY",
    "Fuzz Method": r"FUZZ_HTTP_METHOD"
}

def summarize_logs():
    summary = {key: 0 for key in pattern_map}

    for fname in os.listdir(LOG_DIR):
        if fname.endswith(".txt"):
            path = os.path.join(LOG_DIR, fname)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for key, pattern in pattern_map.items():
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    summary[key] += len(matches)

    total = sum(summary.values())
    log_to_text("[SUMMARY] ShadowScan izvršena analiza svih logova.")
    
    print("\n[+] Rezime detekcija:")
    for key, count in summary.items():
        if count > 0:
            print(f" - {key}: {count}")
    print(f"\n[✓] Ukupno detekcija: {total}")

    return summary

if __name__ == "__main__":
    summarize_logs()
