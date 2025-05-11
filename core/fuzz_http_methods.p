import requests

METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]

def fuzz_methods(url):
    print(f"\n[+] HTTP Method Fuzz test na {url}\n")

    for method in METHODS:
        try:
            r = requests.request(method, url, timeout=5)
            size = len(r.text) if method != "HEAD" else "-"
            print(f"{method:7} => [{r.status_code}] {size} B")
        except Exception as e:
            print(f"{method:7} => [ERR] {e}")
