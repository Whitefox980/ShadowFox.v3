import json
import os

LOG_FILE = "results_log.json"

def search_logs(term=None, severity=None, tool=None, tag=None):
    if not os.path.exists(LOG_FILE):
        print("[!] Nema log fajla.")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    results = []

    for entry in data:
        if term and term.lower() not in entry["output"].lower():
            continue
        if severity and severity.lower() != entry["severity"].lower():
            continue
        if tool and tool.lower() != entry["tool"].lower():
            continue
        if tag and tag.lower() not in [t.lower() for t in entry.get("tags", [])]:
            continue
        results.append(entry)

    if not results:
        print("[!] Nema rezultata za upit.")
        return

    print(f"[✓] Pronađeno {len(results)} rezultata:\n")
    for r in results:
        print(f"{r['timestamp']} | {r['tool']} | {r['target']} | Severity: {r['severity']} | Tags: {', '.join(r.get('tags', []))}")
        print("-" * 80)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Pretraga ShadowFox logova")
    parser.add_argument("--term", help="Tekst koji se traži u output-u")
    parser.add_argument("--severity", help="Npr. High, Medium, Low")
    parser.add_argument("--tool", help="Npr. sqlmap, xss")
    parser.add_argument("--tag", help="Npr. injection, rce, enum")

    args = parser.parse_args()

    search_logs(term=args.term, severity=args.severity, tool=args.tool, tag=args.tag)
