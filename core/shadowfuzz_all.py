from core.fuzz_headers import fuzz_headers
from core.fuzz_param_splitter import fuzz_param_split
from core.fuzz_http_methods import fuzz_methods
from core.fuzz_json_body import fuzz_json

def run_all_fuzz(url):
    print("\n[+] ShadowFuzz AI All-In-One režim")
    print("    → Pokrećem sve fuzzere uz AI analizu...\n")

    # Header
    print("\n--- [1/4] HEADER FUZZ ---")
    fuzz_headers(url)

    # Param Split
    if "FUZZ" in url:
        print("\n--- [2/4] PARAM SPLIT FUZZ ---")
        fuzz_param_split(url)
    else:
        print("[!] Param Split preskočen (nema FUZZ u URL-u)")

    # HTTP Methods
    print("\n--- [3/4] HTTP METHOD FUZZ ---")
    fuzz_methods(url)

    # JSON
    print("\n--- [4/4] JSON BODY FUZZ ---")
    fuzz_json(url)
