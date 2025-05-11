import requests
from urllib.parse import urlencode

TARGET_URL = "http://example.com/redirect?"  # Izmeni ovo

def run_open_redirect_scan():
    payload_url = "http://evil.com"
    full_url = TARGET_URL + urlencode({"next": payload_url})
    try:
        res = requests.get(full_url, allow_redirects=False)
        if "Location" in res.headers and payload_url in res.headers["Location"]:
            print("[!] Moguća Open Redirect ranjivost!")
        else:
            print("[-] Nema redirekcije ka malicioznom URL-u.")
    except Exception as e:
        print(f"[X] Greška: {e}")

if __name__ == "__main__":
    run_open_redirect_scan()
