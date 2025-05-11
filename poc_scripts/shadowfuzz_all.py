import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fuzz_param_splitter import fuzz_param_splitter
from fuzz_json_body import fuzz_json_body
from fuzz_http_methods import fuzz_http_methods
from shadowscan_summary import summarize_logs
from shadow_log_center import generate_ui
from generate_pdf import create_summary_pdf

def shadowfuzz_all(targets):
    print("[*] Pokrećem ShadowFuzz ALL-IN-ONE režim...\n")

    for url in targets:
        print(f"[=] Testiram metu: {url}")
        fuzz_param_splitter(url)
        fuzz_json_body(url)
        fuzz_http_methods(url)

    print("\n[✓] Fuzz moduli završeni.")
    
    print("\n[*] Analiziram logove...")
    summary = summarize_logs()

    print("\n[*] Generišem prikaz kroz Shadow Log Center...")
    generate_ui(summary)

    print("\n[*] Kreiram PDF izveštaj...")
    create_summary_pdf(summary)

    print("\n[✓] ShadowFuzz ALL izvršen kompletno.")

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()

    shadowfuzz_all(targets)
