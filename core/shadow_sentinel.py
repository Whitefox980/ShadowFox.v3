import time
import re
from collections import defaultdict

LOG_PATH = "logs/incoming_hits.log"
MY_IP_PATTERNS = [r"192\.168\.", r"10\.", r"127\.0\.0\.1", r"localhost"]

THRESHOLD = 5  # broj zahteva po IP u kratkom vremenu
ip_activity = defaultdict(int)

def check_payload_for_leak(line):
    for pat in MY_IP_PATTERNS:
        if re.search(pat, line):
            return True
    return False

def monitor_log():
    print("[*] Shadow Sentinel aktivan. Praćenje započeto...\n")
    seen_lines = 0
    while True:
        try:
            with open(LOG_PATH, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            time.sleep(2)
            continue

        new_lines = lines[seen_lines:]
        for line in new_lines:
            if "remote" in line:
                match = re.search(r"'remote': '(.+?)'", line)
                if match:
                    ip = match.group(1)
                    ip_activity[ip] += 1
                    if ip_activity[ip] >= THRESHOLD:
                        print(f"[!] Upozorenje: IP {ip} šalje neuobičajeno mnogo zahteva!")
                        ip_activity[ip] = 0

            if check_payload_for_leak(line):
                print(f"[x] ALARM: Potencijalno curenje tvoje IP adrese otkriveno u payloadu!")
                print(f"    >>> {line.strip()}")

        seen_lines = len(lines)
        time.sleep(3)
