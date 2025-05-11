import os
import json
from datetime import datetime

LOG_FILE = "results_log.json"

def log_result(target, tool, output, status="unknown", severity="unknown", tags=[]):
    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": target,
        "tool": tool,
        "status": status,
        "severity": severity,
        "tags": tags,
        "output": output[:1000]
    }

    data = []

    # Učitaj postojeće ako fajl postoji
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            content = f.read().strip()
            if content:
                try:
                    data = json.loads(content)
                except Exception as e:
                    print(f"[-] Greška pri čitanju JSON loga: {e}")
                    data = []

    data.append(log_data)

    # Zapiši u log fajl
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[+] Logovan rezultat za {tool} na {target}.")
    except Exception as e:
        print(f"[-] Greška pri upisu u log fajl: {e}")
