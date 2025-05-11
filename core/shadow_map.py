import matplotlib.pyplot as plt
import requests
import hashlib
import time
from datetime import datetime
from logics.fuzz_gen import fuzz_payload

DNSLOG_URL = "https://dnslog.cn/getrecords.php"

def dns_triggered():
    try:
        r = requests.get(DNSLOG_URL, timeout=5)
        return "No record" not in r.text
    except:
        return False

def generate_shadowmap(url, base_payload):
    print(f"\n[+] Pokrećem ShadowMap na {url}")
    mutations = fuzz_payload(base_payload)
    baseline = ""

    try:
        baseline = requests.get(url.replace("FUZZ", "base"), timeout=5).text
    except:
        pass

    points = []

    for i, payload in enumerate(mutations, 1):
        full_url = url.replace("FUZZ", payload)
        try:
            r = requests.get(full_url, timeout=5)
            diff = len(r.text) - len(baseline)
            reflected = payload in r.text
            time.sleep(1)
            dns = dns_triggered()

            color = "blue"
            if reflected and dns:
                color = "green"
            elif reflected:
                color = "red"
            elif dns:
                color = "orange"

            points.append((i, diff, color))

        except:
            continue

    if not points:
        print("[x] Nema podataka za mapiranje.")
        return

    # Prikaz
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.figure(figsize=(10,6))
    for x, y, c in points:
        plt.scatter(x, y, color=c, label=c if c not in plt.gca().get_legend_handles_labels()[1] else "")
    plt.title("ShadowFox Payload Map")
    plt.xlabel("Payload #")
    plt.ylabel("Δ response size")
    plt.legend()
    plt.grid(True)
    filename = f"shadowmap_{now}.png"
    plt.savefig(filename)
    print(f"[✓] ShadowMap sačuvan kao {filename}")
try:
        import platform, os
        system = platform.system()
        if system == "Linux":
            os.system(f"xdg-open {filename}")
        elif system == "Darwin":  # macOS
            os.system(f"open {filename}")
        elif system == "Windows":
            os.startfile(filename)
    except:
        pass
