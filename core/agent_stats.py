import json
from collections import Counter, defaultdict

LOG_FILE = "logs/agent_log.jsonl"

def analyze_agent_logs():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = [json.loads(l) for l in f.readlines()]
    except:
        print("[x] Nema logova ili fajl nije čitljiv.")
        return

    if not lines:
        print("[x] Log je prazan.")
        return

    module_counts = Counter()
    reflected_counts = Counter()
    url_hits = defaultdict(int)
    total_size = 0

    for entry in lines:
        module_counts[entry["module"]] += 1
        if entry["reflected"]:
            reflected_counts[entry["module"]] += 1
            url_hits[entry["url"]] += 1
        total_size += entry.get("size", 0)

    print("\n[✓] ShadowAgentX Statistika\n")

    print("Napadi po modulu:")
    for mod, count in module_counts.items():
        print(f"  - {mod}: {count} pokrenutih")

    print("\nRefleksije po modulu:")
    for mod, count in reflected_counts.items():
        print(f"  - {mod}: {count} reflektovanih")

    avg_size = total_size / len(lines)
    print(f"\nProsečna dužina odgovora: {int(avg_size)} B")

    if url_hits:
        print("\nTop 3 mete po refleksiji:")
        for url, count in sorted(url_hits.items(), key=lambda x: -x[1])[:3]:
            print(f"  - {url} ({count} puta)")
