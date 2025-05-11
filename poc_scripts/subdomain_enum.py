import requests
import socket

def run_subdomain_enum(domain, wordlist=None):
    if wordlist is None:
        wordlist = [
            "www", "admin", "mail", "ftp", "dev", "test", "api", "portal",
            "dashboard", "vpn", "db", "beta", "staging"
        ]

    results = []

    for sub in wordlist:
        subdomain = f"{sub}.{domain.replace('http://', '').replace('https://', '').split('/')[0]}"
        try:
            ip = socket.gethostbyname(subdomain)
            url = f"http://{subdomain}"
            res = requests.get(url, timeout=5)
            if res.status_code in [200, 301, 302]:
                results.append({
                    "url": url,
                    "param": sub,
                    "status": res.status_code,
                    "content": res.text
                })
                print(f"[+] Subdomena aktivna: {url} ({res.status_code})")
        except:
            pass  # subdomena ne postoji

    return results
