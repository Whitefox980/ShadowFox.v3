import os
from logics.ai_tools import suggest_exploit, suggest_fix, classify_severity
from tools.shadow_fuzzcore import run_all_fuzz_modules
from tools.shadow_payload_gen import generate_payloads

def run_all():
    print("[*] Pokrećem sve testove za sve mete...")

    try:
        with open("targets/targets.txt", "r") as f:
            targets = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("[-] targets.txt nije pronađen.")
        return

    if not targets:
        print("[-] Nema meta u targets.txt")
        return

    testovi = [
        ("sql_injection", "SQL Injection Tester"),
        ("xss_scanner", "XSS Scanner"),
        ("ssrf_checker", "SSRF Checker"),
        ("open_redirect", "Open Redirect Tester"),
        ("idor_tester", "IDOR Tester"),
        ("command_injection", "Command Injection Scanner"),
        ("lfi_scanner", "LFI Scanner"),
        ("ssti_scanner", "SSTI Scanner"),
        ("csrf_poc", "CSRF Tester"),
        ("dir_brute", "Directory Bruteforce")
    ]

    for target in targets:
        print(f"\n[+] Testiram metu: {target}")
        output = ""
        for skripta, opis in testovi:
            print(f"[*] {opis} ...")
            result = os.popen(f"python poc_scripts/{skripta}.py {target}").read()
            output += f"\n--- {opis} ---\n{result}\n"

        analiza = input("AI analiza? [y/n]: ").strip().lower()
        if analiza == "y":
            try:
                exploit = suggest_exploit(output)
                fix = suggest_fix(output)
                severity = classify_severity(output)

                print(f"\n[+] AI Exploit predlog:\n{exploit}")
                print(f"[+] AI Fix predlog:\n{fix}")
                print(f"[+] Procena ozbiljnosti: {severity}")
            except Exception as e:
                print(f"[!] Greška u AI analizi: {e}")

def run_fuzz_modules():
    print("\n[*] Pokrećem ShadowFuzz AI All-In-One...")
    run_all_fuzz_modules()

def run_payload_generator():
    print("\n[*] Pokrećem ShadowPayload Generator...")
    generate_payloads()
