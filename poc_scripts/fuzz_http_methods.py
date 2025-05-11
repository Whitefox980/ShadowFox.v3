import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from poc_scripts.log_to_text import log_to_text
from poc_scripts.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def fuzz_http_methods(url):
    methods = ["DEBUG", "TRACE", "TRACK", "OPTIONS", "PATCH", "PROPFIND"]
    headers = {
        "User-Agent": "ShadowFox-HTTPMethodsFuzz"
    }

    for method in methods:
        try:
            res = requests.request(method, url, headers=headers, timeout=6)
            if res.status_code < 400:
                log_to_text(f"[FUZZ_HTTP_METHOD] {method} allowed on {url} (Status: {res.status_code})")
                severity = classify_severity(res.text)
                ai_trigger_if_needed("Fuzz HTTP Method", url, method, res.text, severity)
                print(f"[+] Metod '{method}' dozvoljen na {url}")
        except Exception as e:
            print(f"[-] {method} error: {e}")

    print("[-] HTTP metode fuzz završen.")
    return None

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()
    
    for url in urls:
        fuzz_http_methods(url)
