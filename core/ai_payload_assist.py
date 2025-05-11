import requests
import json
from openai import OpenAI

# koristi ENV promenu za ključ
client = OpenAI()

def generate_smart_payload(url):
    print(f"\n[+] Analiziram URL: {url}\n")

    try:
        r = requests.get(url, timeout=5)
        content = r.text[:1000]  # uzmi prvih 1000 karaktera odgovora
    except Exception as e:
        print(f"[x] Ne mogu da dohvatim URL: {e}")
        return

    prompt = f"""
URL: {url}
Response snippet: {content}

Na osnovu ovoga, predloži payload za testiranje bezbednosti.
Možeš izabrati poznat payload iz arsenala (XSS, SQLi, SSRF...) ili generisati novi ako je to prikladno.

Vrati rezultat u JSON formatu:

{{
  "category": "XSS",
  "payload": "<script>alert(1)</script>",
  "description": "Reflected XSS test",
  "reason": "Odgovor sadrži reflektovanu vrednost u HTML kontekstu."
}}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    try:
        raw = response.choices[0].message.content.strip()
        data = json.loads(raw)
        print(f"\n[AI] Preporučen payload:\n")
        print(f"Category : {data['category']}")
        print(f"Payload  : {data['payload']}")
        print(f"Desc     : {data['description']}")
        print(f"Reason   : {data['reason']}")
    except:
        print("[x] Ne mogu da parsiram AI odgovor.")
def generate_and_test_payload(url):
    print(f"\n[+] AI generacija + automatski test na: {url}\n")

    try:
        r = requests.get(url, timeout=5)
        content = r.text[:1000]
    except Exception as e:
        print(f"[x] Ne mogu da dohvatim URL: {e}")
        return

    prompt = f"""
URL: {url}
Response snippet: {content}

Na osnovu ovoga, predloži payload za testiranje bezbednosti (XSS, SQLi, SSRF...).
Vrati kao JSON:

{{
  "category": "XSS",
  "payload": "<script>alert(1)</script>",
  "description": "Reflected XSS test",
  "reason": "HTML kontekst otkriven"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    try:
        raw = response.choices[0].message.content.strip()
        data = json.loads(raw)

        print(f"\n[AI] Preporučen payload:\n")
        print(f"Category : {data['category']}")
        print(f"Payload  : {data['payload']}")
        print(f"Desc     : {data['description']}")
        print(f"Reason   : {data['reason']}")

        # TEST
        test_url = url.replace("FUZZ", data["payload"])
        test_resp = requests.get(test_url, timeout=5)
        reflected = data["payload"] in test_resp.text
        print(f"\n[TEST] Status: {test_resp.status_code} | Reflektovan: {'DA' if reflected else 'ne'}")

    except Exception as e:
        print(f"[x] Ne mogu da parsiram ili testiram: {e}")
