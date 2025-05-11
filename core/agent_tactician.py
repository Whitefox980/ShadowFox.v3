import json
from collections import Counter, defaultdict
from openai import OpenAI

client = OpenAI()

def analyze_and_suggest_tactics(log_file="logs/agent_log.jsonl"):
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = [json.loads(l) for l in f.readlines()]
    except:
        print("[x] Nema log fajla.")
        return

    if not logs:
        print("[x] Log je prazan.")
        return

    # Sažetak za prompt
    summary = []

    for entry in logs:
        summary.append({
            "module": entry["module"],
            "reflected": entry["reflected"],
            "url": entry["url"],
            "payload": entry["payload"],
            "size": entry.get("size", 0)
        })

    prompt = f"""
Ti si AI taktički analitičar. Na osnovu ovih rezultata ShadowAgentX napada, predloži:

1. Koji fuzz moduli daju najbolje rezultate?
2. Koje vrste payload-a (ili obrasci) su najuspešniji?
3. Koje mete su najosetljivije?
4. Taktika za sledeći ciklus skeniranja (šta da koristi više, šta manje)

Rezultati:
{json.dumps(summary[-50:], indent=2)}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    print("\n[AI TAKTIKA]:\n")
    print(response.choices[0].message.content.strip())
