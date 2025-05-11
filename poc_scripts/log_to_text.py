import datetime
import os

def log_to_text(module_name, content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    filename = os.path.join(log_dir, f"log_{os.path.basename(module_name)}.txt")

    with open(filename, "a") as f:
        f.write(f"[{timestamp}] {content}\n")

def classify_severity(content):
    content_lower = content.lower()
    if "critical" in content_lower or "rce" in content_lower:
        return "CRITICAL"
    elif "xss" in content_lower or "sql" in content_lower:
        return "HIGH"
    elif "idor" in content_lower or "open redirect" in content_lower:
        return "MEDIUM"
    else:
        return "LOW"
