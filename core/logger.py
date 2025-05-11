import json
import os
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
        "output": output.strip()[:1000]
    }

    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
            except Exception:
                data = []

    data.append(log_data)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[+] Logovan rezultat za {tool} na {target}.")
