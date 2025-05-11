import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dir_brute import dir_brute
from param_discovery import discover_params
from hidden_param_brute import brute_hidden_params
from method_discovery import discover_methods
from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

try:
    from subdomain_enum import run_subdomain_enum
    SUBENUM_ENABLED = True
except ImportError:
    SUBENUM_ENABLED = False

def trigger_from_result(module_name, result):
    url = result.get("url", "")
    payload = result.get("param", "") or result.get("status", "")
    content = result.get("content", "")
    severity = classify_severity(content)
    ai_trigger_if_needed(module_name, url, payload, content, severity)

def shadowrecon_all(targets):
    print("[*] Pokrećem SHADOWRECON fazu...\n")

    for url in targets:
        print(f"[=] Meta: {url}")

        for result in dir_brute(url):
            trigger_from_result("Dir Brute", result)

        for result in discover_params(url):
            trigger_from_result("Param Discovery", result)

        for result in brute_hidden_params(url):
            trigger_from_result("Hidden Param", result)

        for result in discover_methods(url):
            trigger_from_result("HTTP Method", result)

        if SUBENUM_ENABLED:
            for result in run_subdomain_enum(url):
                trigger_from_result("Subdomain Enum", result)

    log_to_text("[RECON] ShadowRecon završio analizu.")
    print("\n[✓] ShadowRecon ALL završeno.")

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()

    shadowrecon_all(urls)
