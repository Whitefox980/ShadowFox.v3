import requests
from datetime import datetime

TARGET = "http://example.com"  # Izmeni!
WORDLIST = ["admin", "login", "dashboard", "backup", "config"]

print(f"[{datetime.now()}] DirBrute start za: {TARGET}")
for word in WORDLIST:
    url = f"{TARGET}/{word}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print(f"[+] FOUND: {url}")
        else:
            print(f"[-] {url} => {r.status_code}")
    except requests.RequestException as e:
        print(f"[!] ERROR: {e}")
