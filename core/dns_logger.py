import requests
import time

DNS_LOG_URL = "https://dnslog.cn/getrecords.php"  # možeš promeniti na svoj DNS log servis

def check_dns_logs():
    print("[*] Proveravam DNS logove sa dnslog.cn...")
    try:
        r = requests.get(DNS_LOG_URL, timeout=10)
        if "No record" in r.text:
            print("[x] Nema DNS upita za sada.")
        else:
            print("[✓] DNS upit detektovan!")
            print(r.text)
    except Exception as e:
        print(f"[!] Greška: {str(e)}")

def monitor_dns(interval=15, tries=5):
    print(f"[+] Pokrećem pasivni monitoring DNS-a ({tries} pokušaja, {interval}s)...\n")
    for i in range(tries):
        print(f"--- Pokušaj {i+1}/{tries} ---")
        check_dns_logs()
        time.sleep(interval)
