import json
import os
from datetime import datetime

results_dir = "results/json"
os.makedirs(results_dir, exist_ok=True)

export_path = os.path.join(results_dir, "vulnerabilities_export.json")

# Primer strukture - možeš zameniti svojim dinamičkim logovima
vulnerabilities = [
    {
        "type": "SQL Injection",
        "target": "http://testphp.vulnweb.com?id=' OR '1'='1",
        "severity": "high",
        "timestamp": datetime.now().isoformat()
    },
    {
        "type": "XSS",
        "target": "http://example.com/page.php?query=<script>alert(1)</script>",
        "severity": "medium",
        "timestamp": datetime.now().isoformat()
    }
]

with open(export_path, "w") as f:
    json.dump(vulnerabilities, f, indent=4)

print(f"[+] Ranjivosti eksportovane u {export_path}")
