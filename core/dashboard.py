import json
import os
import sys

def show_dashboard(severity_filter=None, tool_filter=None):
    log_file = "results_log.json"
    if not os.path.exists(log_file):
        print("[!] Nema log fajla.")
        return

    with open(log_file, "r") as f:
        data = json.load(f)

    if severity_filter:
        data = [r for r in data if r['severity'].lower() == severity_filter.lower()]
    if tool_filter:
        data = [r for r in data if r['tool'].lower() == tool_filter.lower()]

    print("="*100)
    print(f"{'VREME':<20} | {'META':<25} | {'ALAT':<10} | {'STATUS':<10} | {'SEVERITY':<10}")
    print("="*100)

    for r in data:
        print(f"{r['timestamp']:<20} | {r['target']:<25} | {r['tool']:<10} | {r['status']:<10} | {r['severity']:<10}")

    print("="*100)
    print(f"Ukupno: {len(data)}")

if __name__ == "__main__":
    severity = None
    tool = None

    if "--severity" in sys.argv:
        i = sys.argv.index("--severity")
        if i + 1 < len(sys.argv):
            severity = sys.argv[i+1]

    if "--tool" in sys.argv:
        i = sys.argv.index("--tool")
        if i + 1 < len(sys.argv):
            tool = sys.argv[i+1]

    show_dashboard(severity, tool)
