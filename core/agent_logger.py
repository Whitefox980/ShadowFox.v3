import json
from datetime import datetime

LOG_FILE = "logs/agent_log.jsonl"

def log_agent_action(url, module, payload, status, reflected, reason, result_size):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "url": url,
        "module": module,
        "payload": payload,
        "status": status,
        "reflected": reflected,
        "size": result_size,
        "reason": reason
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"[LOG] Zapisano u agent_log.jsonl")
