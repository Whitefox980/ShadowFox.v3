
# shadow_check.py
print("\n[+] ShadowFox Sanity Check\n")

checks = [
    ("poc_scripts.shadowfuzz_all", "shadowfuzz_all"),
    ("poc_scripts.shadowscan_summary", "summarize_logs"),
    ("poc_scripts.generate_pdf", "generate_pdf_from_logs"),
    ("poc_scripts.log_to_text", "log_to_text"),
    ("logics.fuzz_ai_trigger", "ai_trigger_if_needed"),
    ("tools.auto_add_severity", "classify_severity"),
]

for mod, func in checks:
    try:
        module = __import__(mod, fromlist=[func])
        if hasattr(module, func):
            print(f"[OK] {mod}.{func}")
        else:
            print(f"[X] {mod} postoji, ali nedostaje {func}")
    except Exception as e:
        print(f"[X] Ne može da se uveze {mod}: {e}")

