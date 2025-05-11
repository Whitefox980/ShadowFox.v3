import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def dir_brute(url, wordlist=None):
    if wordlist is None:
        wordlist = [
            "admin", "login", "uploads", "config", "backup",
            ".git", ".env", "private", "test", "old"
        ]

    headers = {"User-Agent": "ShadowFox-DirBrute"}
    results = []

    for word in wordlist:
        test_url = f"{url.rstrip('/')}/{word}"
        try:
            res = requests.get(test_url, headers=headers, timeout=6)
            if res.status_code in [200, 401, 403]:
                results.append({
                    "url": test_url,
                    "status": res.status_code,
                    "content": res.text,
                    "param": word
                })
                print(f"[+] DirBrute pogodak: {test_url} ({res.status_code})")
        except Exception as e:
            print(f"[-] Greška kod {test_url}: {e}")

    return results
if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        urls = f.read().splitlines()

    shadowrecon_all(urls)
