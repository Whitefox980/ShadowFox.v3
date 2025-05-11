import requests

domain = "example.com"
subdomains = ["admin", "mail", "ftp", "test", "dev", "vpn"]
found = []

for sub in subdomains:
    url = f"http://{sub}.{domain}"
    try:
        res = requests.get(url, timeout=2)
        print(f"[+] Found: {url} - Status: {res.status_code}")
        found.append(url)
    except:
        pass

with open("reports/found_subdomains.txt", "w") as f:
    for sub in found:
        f.write(sub + "\n")
